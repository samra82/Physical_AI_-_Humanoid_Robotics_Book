import json
import os
import time
from datetime import datetime
from typing import Dict, List, Any
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class QueryReport:
    """Data class to store query report information"""
    query_id: str
    query_text: str
    response: str
    sources: List[str]
    confidence_score: float
    query_time_ms: float
    timestamp: str
    similarity_scores: List[float]
    retrieved_chunks_count: int
    context_length: int
    session_id: str = None
    user_feedback: str = None  # 'positive', 'negative', or None


class RAGReportGenerator:
    """Generates reports and analytics for the RAG system"""

    def __init__(self, reports_dir: str = "reports"):
        self.reports_dir = Path(reports_dir)
        self.reports_dir.mkdir(exist_ok=True)

        # Initialize report files
        self.queries_log_path = self.reports_dir / "queries_log.jsonl"
        self.queries_log_path.touch(exist_ok=True)

        self.metrics_path = self.reports_dir / "metrics.json"
        self.metrics_path.touch(exist_ok=True)

    def log_query(self, query_report: QueryReport):
        """Log a query to the queries log file"""
        with open(self.queries_log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(asdict(query_report)) + '\n')

    def update_metrics(self, query_report: QueryReport):
        """Update aggregated metrics based on the query"""
        # Load existing metrics
        metrics = self._load_metrics()

        # Update metrics
        metrics['total_queries'] = metrics.get('total_queries', 0) + 1
        metrics['total_query_time'] = metrics.get('total_query_time', 0) + query_report.query_time_ms
        metrics['avg_query_time'] = metrics['total_query_time'] / metrics['total_queries']

        # Update confidence metrics
        if 'confidence_scores' not in metrics:
            metrics['confidence_scores'] = []
        metrics['confidence_scores'].append(query_report.confidence_score)

        # Calculate average confidence
        avg_confidence = sum(metrics['confidence_scores']) / len(metrics['confidence_scores'])
        metrics['avg_confidence'] = avg_confidence

        # Update context metrics
        if 'context_lengths' not in metrics:
            metrics['context_lengths'] = []
        metrics['context_lengths'].append(query_report.context_length)

        # Calculate average context length
        avg_context_length = sum(metrics['context_lengths']) / len(metrics['context_lengths'])
        metrics['avg_context_length'] = avg_context_length

        # Update retrieved chunks metrics
        if 'retrieved_chunks_counts' not in metrics:
            metrics['retrieved_chunks_counts'] = []
        metrics['retrieved_chunks_counts'].append(query_report.retrieved_chunks_count)

        # Calculate average retrieved chunks
        avg_retrieved_chunks = sum(metrics['retrieved_chunks_counts']) / len(metrics['retrieved_chunks_counts'])
        metrics['avg_retrieved_chunks'] = avg_retrieved_chunks

        # Update feedback metrics
        if query_report.user_feedback:
            if 'feedback_counts' not in metrics:
                metrics['feedback_counts'] = {'positive': 0, 'negative': 0}
            metrics['feedback_counts'][query_report.user_feedback] = \
                metrics['feedback_counts'].get(query_report.user_feedback, 0) + 1

        # Save updated metrics
        with open(self.metrics_path, 'w', encoding='utf-8') as f:
            json.dump(metrics, f, indent=2)

    def _load_metrics(self) -> Dict[str, Any]:
        """Load existing metrics from file"""
        try:
            with open(self.metrics_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def generate_daily_report(self, date: str = None) -> Dict[str, Any]:
        """Generate a daily report for the specified date (or today)"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')

        # Load all queries
        queries = self._load_queries_for_date(date)

        if not queries:
            return {
                'date': date,
                'summary': 'No queries found for this date',
                'metrics': {}
            }

        # Calculate daily metrics
        total_queries = len(queries)
        total_time = sum(q['query_time_ms'] for q in queries)
        avg_time = total_time / total_queries
        avg_confidence = sum(q['confidence_score'] for q in queries) / total_queries
        avg_context_length = sum(q['context_length'] for q in queries) / total_queries
        avg_retrieved_chunks = sum(q['retrieved_chunks_count'] for q in queries) / total_queries

        # Feedback summary
        feedback_counts = {'positive': 0, 'negative': 0, 'none': 0}
        for q in queries:
            feedback = q.get('user_feedback', 'none')
            feedback_counts[feedback] += 1

        report = {
            'date': date,
            'summary': f'Daily report for {date}',
            'metrics': {
                'total_queries': total_queries,
                'avg_response_time_ms': avg_time,
                'avg_confidence_score': avg_confidence,
                'avg_context_length': avg_context_length,
                'avg_retrieved_chunks': avg_retrieved_chunks,
                'feedback_summary': feedback_counts
            },
            'top_queries': sorted(queries, key=lambda x: x['query_time_ms'], reverse=True)[:5],
            'low_confidence_queries': [q for q in queries if q['confidence_score'] < 0.5]
        }

        return report

    def _load_queries_for_date(self, date: str) -> List[Dict]:
        """Load queries for a specific date"""
        queries = []
        try:
            with open(self.queries_log_path, 'r', encoding='utf-8') as f:
                for line in f:
                    query_data = json.loads(line.strip())
                    query_date = query_data['timestamp'][:10]  # Extract date part
                    if query_date == date:
                        queries.append(query_data)
        except FileNotFoundError:
            pass

        return queries

    def generate_feedback_report(self) -> Dict[str, Any]:
        """Generate a report on user feedback"""
        queries = []
        try:
            with open(self.queries_log_path, 'r', encoding='utf-8') as f:
                for line in f:
                    query_data = json.loads(line.strip())
                    if query_data.get('user_feedback'):
                        queries.append(query_data)
        except FileNotFoundError:
            pass

        if not queries:
            return {'summary': 'No feedback received yet'}

        feedback_counts = {'positive': 0, 'negative': 0}
        for q in queries:
            feedback = q.get('user_feedback', 'none')
            if feedback in feedback_counts:
                feedback_counts[feedback] += 1

        # Find most common positive and negative queries
        positive_queries = [q for q in queries if q.get('user_feedback') == 'positive']
        negative_queries = [q for q in queries if q.get('user_feedback') == 'negative']

        return {
            'total_feedback': len(queries),
            'feedback_counts': feedback_counts,
            'positive_ratio': feedback_counts['positive'] / len(queries) if queries else 0,
            'top_positive_queries': positive_queries[:10],
            'top_negative_queries': negative_queries[:10]
        }

    def export_report(self, report: Dict[str, Any], filename: str):
        """Export a report to a JSON file"""
        filepath = self.reports_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        return filepath


# Example usage
if __name__ == "__main__":
    # Create a report generator
    reporter = RAGReportGenerator()

    # Example of logging a query
    query_report = QueryReport(
        query_id="test-123",
        query_text="What is ROS2?",
        response="ROS2 is a robotics framework...",
        sources=["https://test-book.com/ros2-intro"],
        confidence_score=0.85,
        query_time_ms=125.5,
        timestamp=datetime.now().isoformat(),
        similarity_scores=[0.85, 0.72, 0.68],
        retrieved_chunks_count=3,
        context_length=1200,
        session_id="session-abc",
        user_feedback="positive"
    )

    reporter.log_query(query_report)
    reporter.update_metrics(query_report)

    # Generate reports
    daily_report = reporter.generate_daily_report()
    feedback_report = reporter.generate_feedback_report()

    # Export reports
    daily_path = reporter.export_report(daily_report, f"daily_report_{datetime.now().strftime('%Y%m%d')}.json")
    feedback_path = reporter.export_report(feedback_report, "feedback_report.json")

    print(f"Reports generated:")
    print(f"  Daily report: {daily_path}")
    print(f"  Feedback report: {feedback_path}")