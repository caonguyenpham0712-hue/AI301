import json
import os
import pandas as pd
from datetime import datetime

class DataLoader:
    def __init__(self, data_dir="data", benchmark_date="2026-11-15"):
        self.data_dir = data_dir
        self.benchmark_date = datetime.strptime(benchmark_date, "%Y-%m-%d")
        
        self.contracts_df = None
        self.usage_df = None
        self.tickets_df = None
        self.service_packages = None
        self.discount_policies = None
        self.unified_df = None

    def load_all(self):
        """Load and harmonize all data files into structured DataFrames."""
        # Load JSON configurations
        with open(os.path.join(self.data_dir, "service_packages.json"), "r", encoding="utf-8") as f:
            self.service_packages = json.load(f)
            
        with open(os.path.join(self.data_dir, "discount_policies.json"), "r", encoding="utf-8") as f:
            self.discount_policies = json.load(f)

        # Load CSVs
        self.contracts_df = pd.read_csv(os.path.join(self.data_dir, "contracts.csv"), encoding="utf-8")
        self.usage_df = pd.read_csv(os.path.join(self.data_dir, "usage_logs.csv"), encoding="utf-8")
        self.tickets_df = pd.read_csv(os.path.join(self.data_dir, "support_tickets.csv"), encoding="utf-8")

        # Parse dates
        self.contracts_df["contract_start_date"] = pd.to_datetime(self.contracts_df["contract_start_date"])
        self.contracts_df["contract_end_date"] = pd.to_datetime(self.contracts_df["contract_end_date"])
        self.usage_df["last_active_date"] = pd.to_datetime(self.usage_df["last_active_date"])
        self.tickets_df["created_at"] = pd.to_datetime(self.tickets_df["created_at"])
        self.tickets_df["resolved_at"] = pd.to_datetime(self.tickets_df["resolved_at"], errors="coerce")

        # Aggregate tickets per customer
        ticket_summary = self._aggregate_tickets()

        # Merge contracts + usage + aggregated tickets
        merged = pd.merge(self.contracts_df, self.usage_df, on="customer_id", how="left", suffixes=("", "_usage"))
        merged = pd.merge(merged, ticket_summary, on="customer_id", how="left")

        # Fill NAs for customers with 0 tickets
        merged["total_tickets"] = merged["total_tickets"].fillna(0).astype(int)
        merged["open_tickets"] = merged["open_tickets"].fillna(0).astype(int)
        merged["p1_p2_open_tickets"] = merged["p1_p2_open_tickets"].fillna(0).astype(int)
        merged["avg_csat"] = merged["avg_csat"].fillna(5.0)  # Default good rating if no complaints
        merged["has_unresolved_critical_incident"] = merged["p1_p2_open_tickets"] > 0

        # Calculate time metrics based on benchmark_date
        merged["days_until_expiry"] = (merged["contract_end_date"] - self.benchmark_date).dt.days
        
        # Lead time: Enterprise needs 45 days, Standard/Professional needs 30 days
        merged["required_lead_days"] = merged["current_package"].apply(
            lambda pkg: 45 if pkg == "Enterprise" else 30
        )
        
        merged["target_contact_date"] = merged["contract_end_date"] - pd.to_timedelta(merged["required_lead_days"], unit="D")
        merged["days_until_contact_due"] = (merged["target_contact_date"] - self.benchmark_date).dt.days

        self.unified_df = merged
        return self.unified_df

    def _aggregate_tickets(self):
        """Aggregate support tickets per customer."""
        df = self.tickets_df.copy()
        df["is_open"] = df["status"].isin(["Open", "In_Progress"])
        df["is_p1_p2"] = df["severity"].str.contains("P1|P2", case=False, na=False)
        df["is_p1_p2_open"] = df["is_open"] & df["is_p1_p2"]

        grouped = df.groupby("customer_id").agg(
            total_tickets=("ticket_id", "count"),
            open_tickets=("is_open", "sum"),
            p1_p2_open_tickets=("is_p1_p2_open", "sum"),
            avg_csat=("csat_score", lambda x: pd.to_numeric(x, errors="coerce").mean())
        ).reset_index()

        return grouped

