#!/usr/bin/env python3
"""
Report Generator for RAG System
This script generates various reports about the RAG system's performance
"""

import argparse
from reports import RAGReportGenerator
import json
from datetime import datetime


def main():
    parser = argparse.ArgumentParser(description='Generate reports for the RAG system')
    parser.add_argument('--type', choices=['daily', 'feedback', 'metrics'],
                        default='daily', help='Type of report to generate')
    parser.add_argument('--date', type=str, help='Date for daily report (YYYY-MM-DD)')
    parser.add_argument('--output', type=str, help='Output file for the report')

    args = parser.parse_args()

    reporter = RAGReportGenerator()

    if args.type == 'daily':
        date = args.date or datetime.now().strftime('%Y-%m-%d')
        report = reporter.generate_daily_report(date)
        print("Daily Report:")
        print(json.dumps(report, indent=2))

    elif args.type == 'feedback':
        report = reporter.generate_feedback_report()
        print("Feedback Report:")
        print(json.dumps(report, indent=2))

    elif args.type == 'metrics':
        metrics = reporter._load_metrics()
        print("Metrics Report:")
        print(json.dumps(metrics, indent=2))

    if args.output:
        filepath = reporter.export_report(report if args.type != 'metrics' else metrics, args.output)
        print(f"Report exported to: {filepath}")


if __name__ == "__main__":
    main()