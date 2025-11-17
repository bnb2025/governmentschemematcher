"""
BigQuery Analytics Module - Handles database queries and analytics
"""

from typing import List, Dict, Optional
from google.cloud import bigquery
from config.gcp_config import gcp_config


class BigQueryAnalytics:
    """Handles BigQuery queries and analytics"""
    
    def __init__(self, project_id: Optional[str] = None):
        """
        Initialize BigQuery Analytics
        
        Args:
            project_id: GCP project ID (default from config)
        """
        self.project_id = project_id or gcp_config.GCP_PROJECT_ID
        self.dataset_id = gcp_config.BIGQUERY_DATASET
        self.table_id = gcp_config.BIGQUERY_TABLE
        self.client = bigquery.Client(project=self.project_id)
    
    def execute_query(self, query: str, max_results: int = 10) -> Optional[List[Dict]]:
        """
        Execute a BigQuery query
        
        Args:
            query: SQL query to execute
            max_results: Maximum number of results to return
            
        Returns:
            List of query results as dictionaries
        """
        try:
            job_config = bigquery.QueryJobConfig(max_results=max_results)
            query_job = self.client.query(query, job_config=job_config)
            
            results = []
            for row in query_job:
                results.append(dict(row.items()))
            
            return results
            
        except Exception as e:
            print(f"❌ Error executing query: {e}")
            return None
    
    def get_scheme_info(self, scheme_name: Optional[str] = None) -> Optional[List[Dict]]:
        """
        Get information about government schemes
        
        Args:
            scheme_name: Optional scheme name to filter by
            
        Returns:
            List of scheme information
        """
        try:
            if scheme_name:
                query = f"""
                SELECT * FROM `{self.project_id}.{self.dataset_id}.{self.table_id}`
                WHERE LOWER(scheme_name) LIKE LOWER('%{scheme_name}%')
                LIMIT 10
                """
            else:
                query = f"""
                SELECT * FROM `{self.project_id}.{self.dataset_id}.{self.table_id}`
                LIMIT 10
                """
            
            return self.execute_query(query)
            
        except Exception as e:
            print(f"❌ Error fetching scheme info: {e}")
            return None
    
    def search_schemes_by_criteria(
        self,
        criteria: Dict[str, str]
    ) -> Optional[List[Dict]]:
        """
        Search schemes by multiple criteria
        
        Args:
            criteria: Dictionary of search criteria (e.g., {'category': 'education'})
            
        Returns:
            List of matching schemes
        """
        try:
            where_clauses = []
            for key, value in criteria.items():
                where_clauses.append(f"LOWER({key}) LIKE LOWER('%{value}%')")
            
            where_clause = " AND ".join(where_clauses)
            
            query = f"""
            SELECT * FROM `{self.project_id}.{self.dataset_id}.{self.table_id}`
            WHERE {where_clause}
            LIMIT 20
            """
            
            return self.execute_query(query, max_results=20)
            
        except Exception as e:
            print(f"❌ Error searching schemes: {e}")
            return None
    
    def get_scheme_statistics(self) -> Optional[Dict]:
        """Get statistics about schemes in the database"""
        try:
            query = f"""
            SELECT
                COUNT(*) as total_schemes,
                COUNT(DISTINCT category) as total_categories
            FROM `{self.project_id}.{self.dataset_id}.{self.table_id}`
            """
            
            results = self.execute_query(query, max_results=1)
            return results[0] if results else None
            
        except Exception as e:
            print(f"❌ Error getting statistics: {e}")
            return None
    
    def test_connection(self) -> bool:
        """Test BigQuery connection"""
        try:
            self.client.list_datasets()
            print(f"✓ Successfully connected to BigQuery project: {self.project_id}")
            return True
        except Exception as e:
            print(f"❌ Failed to connect to BigQuery: {e}")
            return False
