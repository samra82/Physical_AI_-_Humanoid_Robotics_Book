import pytest
import os
import tempfile
from unittest.mock import Mock, patch
from reports import RAGReportGenerator, QueryReport
from datetime import datetime


class TestRAGReportGenerator:
    """Test cases for the RAGReportGenerator class"""

    def setup_method(self):
        """Set up test fixtures before each test method"""
        # Create a temporary directory for test reports
        self.temp_dir = tempfile.mkdtemp()
        self.reporter = RAGReportGenerator(reports_dir=self.temp_dir)

    def test_log_query(self):
        """Test logging a query to the report system"""
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
            session_id="session-abc"
        )

        self.reporter.log_query(query_report)

        # Verify the query was logged
        queries = []
        with open(self.reporter.queries_log_path, 'r', encoding='utf-8') as f:
            for line in f:
                queries.append(line.strip())

        assert len(queries) == 1
        logged_query = eval(queries[0])  # In a real test, use json.loads
        assert logged_query['query_id'] == "test-123"
        assert logged_query['query_text'] == "What is ROS2?"
        assert logged_query['confidence_score'] == 0.85

    def test_update_metrics(self):
        """Test updating metrics with a query report"""
        query_report = QueryReport(
            query_id="test-456",
            query_text="What is AI?",
            response="AI is artificial intelligence...",
            sources=["https://test-book.com/ai-intro"],
            confidence_score=0.75,
            query_time_ms=200.0,
            timestamp=datetime.now().isoformat(),
            similarity_scores=[0.75, 0.65],
            retrieved_chunks_count=2,
            context_length=800,
            session_id="session-xyz"
        )

        self.reporter.update_metrics(query_report)

        # Load and verify metrics
        metrics = self.reporter._load_metrics()
        assert metrics['total_queries'] == 1
        assert metrics['total_query_time'] == 200.0
        assert metrics['avg_query_time'] == 200.0
        assert metrics['avg_confidence'] == 0.75
        assert metrics['avg_context_length'] == 800
        assert metrics['avg_retrieved_chunks'] == 2

    def test_generate_daily_report(self):
        """Test generating a daily report"""
        # Add a few test queries
        query_report1 = QueryReport(
            query_id="test-789",
            query_text="What is machine learning?",
            response="Machine learning is...",
            sources=["https://test-book.com/ml-intro"],
            confidence_score=0.80,
            query_time_ms=150.0,
            timestamp=datetime.now().strftime('%Y-%m-%d') + "T10:00:00",
            similarity_scores=[0.80, 0.75],
            retrieved_chunks_count=2,
            context_length=1000,
            session_id="session-123"
        )

        query_report2 = QueryReport(
            query_id="test-999",
            query_text="How does ROS2 work?",
            response="ROS2 works by...",
            sources=["https://test-book.com/ros2-working"],
            confidence_score=0.90,
            query_time_ms=180.0,
            timestamp=datetime.now().strftime('%Y-%m-%d') + "T11:00:00",
            similarity_scores=[0.90, 0.85, 0.80],
            retrieved_chunks_count=3,
            context_length=1200,
            session_id="session-456"
        )

        self.reporter.log_query(query_report1)
        self.reporter.log_query(query_report2)
        self.reporter.update_metrics(query_report1)
        self.reporter.update_metrics(query_report2)

        # Generate daily report for today
        report = self.reporter.generate_daily_report()

        assert report['date'] == datetime.now().strftime('%Y-%m-%d')
        assert report['metrics']['total_queries'] == 2
        assert abs(report['metrics']['avg_response_time_ms'] - 165.0) < 0.01  # (150+180)/2
        assert abs(report['metrics']['avg_confidence_score'] - 0.85) < 0.01  # (0.80+0.90)/2

    def test_generate_feedback_report(self):
        """Test generating a feedback report"""
        # Add queries with feedback
        query_report1 = QueryReport(
            query_id="feedback-1",
            query_text="What is feedback?",
            response="Feedback is important...",
            sources=["https://test-book.com/feedback"],
            confidence_score=0.85,
            query_time_ms=100.0,
            timestamp=datetime.now().isoformat(),
            similarity_scores=[0.85],
            retrieved_chunks_count=1,
            context_length=500,
            session_id="session-feedback",
            user_feedback="positive"
        )

        query_report2 = QueryReport(
            query_id="feedback-2",
            query_text="Negative feedback test",
            response="This is a test...",
            sources=["https://test-book.com/test"],
            confidence_score=0.30,
            query_time_ms=200.0,
            timestamp=datetime.now().isoformat(),
            similarity_scores=[0.30],
            retrieved_chunks_count=1,
            context_length=300,
            session_id="session-feedback2",
            user_feedback="negative"
        )

        self.reporter.log_query(query_report1)
        self.reporter.log_query(query_report2)

        feedback_report = self.reporter.generate_feedback_report()

        assert feedback_report['total_feedback'] == 2
        assert feedback_report['feedback_counts']['positive'] == 1
        assert feedback_report['feedback_counts']['negative'] == 1
        assert abs(feedback_report['positive_ratio'] - 0.5) < 0.01  # 1 out of 2

    def teardown_method(self):
        """Clean up after each test method"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)