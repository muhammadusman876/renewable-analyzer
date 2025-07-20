"""
Policy Manager - Handles policy document loading and context management
"""
from typing import List, Dict
import os


class PolicyManager:
 """
 Manages German energy policy documents and regulatory information
 """

 def __init__(self, policy_docs_path: str):
 self.policy_docs_path = policy_docs_path
 self._cached_documents = None

 def load_policy_documents(self) -> List[str]:
 """Load German energy policy documents for context"""
 if self._cached_documents:
 return self._cached_documents

 # Try to load from files first
 file_documents = self._load_from_files()

 # Always include hardcoded policy information as baseline
 hardcoded_documents = self._get_hardcoded_policy_info()

 # Combine file-based and hardcoded documents
 all_documents = file_documents + hardcoded_documents

 # Additional technical and regulatory knowledge
 additional_docs = self._get_additional_context()
 all_documents.extend(additional_docs)

 self._cached_documents = all_documents
 return all_documents

 def _load_from_files(self) -> List[str]:
 """Load policy documents from files if available"""
 documents = []

 if not os.path.exists(self.policy_docs_path):
 print(f"INFO: Policy documents directory not found: {self.policy_docs_path}")
 return documents

 try:
 for filename in os.listdir(self.policy_docs_path):
 if filename.endswith(('.txt', '.md')):
 file_path = os.path.join(self.policy_docs_path, filename)
 with open(file_path, 'r', encoding='utf-8') as f:
 content = f.read().strip()
 if content:
 documents.append(content)
 print(f"INFO: Loaded policy document: {filename}")
 except Exception as e:
 print(f"WARNING: Error loading policy documents: {e}")

 return documents

 def _get_hardcoded_policy_info(self) -> List[str]:
 """Get baseline German energy policy information"""
 return [
 """
 German Renewable Energy Act (EEG 2023):
 - Feed-in tariffs for solar installations under 10kW: €0.082/kWh
 - No VAT (Mehrwertsteuer) on solar installations since January 2023
 - Simplified registration process for installations under 30kW
 - Net metering allowed for self-consumption optimization
 - Annual compensation adjustments based on market conditions
 """,
 """
 KfW Funding Program 270 (Renewable Energy Standard):
 - Low-interest loans up to €50,000 per installation
 - Financing up to 100% of eligible costs
 - Interest rates starting from 5.03% effective annual rate
 - Repayment terms up to 30 years with up to 3 grace years
 - Additional grants available for energy storage systems
 """,
 """
 Regional Incentives (2024-2025):
 - Bavaria: Additional subsidies up to €3,200 for battery storage
 - Baden-Württemberg: Solar roof programs with up to €1,500 support
 - North Rhine-Westphalia: progres.nrw program with installation grants
 - Berlin: SolarPLUS program with up to €15,000 for installations with storage
 - Schleswig-Holstein: Klimaschutz-Förderung with bonus payments
 """
 ]

 def _get_additional_context(self) -> List[str]:
 """Get additional technical and market context"""
 return [
 """
 Solar Panel Technology Guide:
 - Monocrystalline panels: 20-22% efficiency, higher cost, better performance in low light
 - Polycrystalline panels: 15-17% efficiency, lower cost, good value for money
 - Thin-film panels: 10-12% efficiency, lowest cost, flexible installation options
 - Bifacial panels: Up to 30% more energy yield, suitable for ground-mount systems
 - Perovskite tandem cells: Emerging technology with 30%+ efficiency potential
 """,
 """
 German Installation Requirements:
 - Building permits required for systems over 30kW
 - Structural assessment mandatory for roof-mounted systems
 - Grid connection approval from local utility (Netzbetreiber)
 - Mandatory insurance coverage for systems over 10kW
 - Annual safety inspections for commercial installations
 - Electrical installation by certified Elektrofachkraft required
 """,
 """
 Financing Options in Germany:
 - KfW 270: Standard renewable energy loan, up to €50,000
 - Regional programs: Bavaria, NRW, Baden-Württemberg offer additional grants
 - Solar leasing: No upfront costs, 10-20 year contracts
 - Power purchase agreements (PPA): Long-term electricity contracts
 - Self-financing: Tax benefits through accelerated depreciation
 - Community solar: Shared ownership models gaining popularity
 """,
 """
 Weather and Performance Data:
 - Germany average: 1,000-1,200 kWh/kWp annually
 - North Germany: 950-1,100 kWh/kWp (lower solar irradiance)
 - South Germany: 1,100-1,300 kWh/kWp (higher solar irradiance)
 - Seasonal variation: 60% of annual production in April-September
 - Performance degradation: 0.5-0.8% per year typical
 - Weather insurance available for production guarantees
 """
 ]

 def get_policy_summary(self) -> Dict[str, str]:
 """Get summary of current German solar policies"""
 return {
 "feed_in_tariff": "€0.082/kWh for systems under 10kW",
 "vat_rate": "0% VAT on solar installations since 2023",
 "kfw_financing": "Low-interest loans up to €50,000",
 "net_metering": "Allowed for self-consumption optimization",
 "simplified_approval": "Streamlined process for systems under 30kW",
 "regional_incentives": "Additional grants available in most German states",
 "insurance_requirement": "Mandatory for systems over 10kW"
 }

 def search_policy_context(self, query: str) -> List[str]:
 """Search for relevant policy documents based on query keywords"""
 documents = self.load_policy_documents()
 relevant_docs = []

 # Simple keyword matching - can be enhanced with semantic search
 query_lower = query.lower()
 keywords = query_lower.split()

 for doc in documents:
 doc_lower = doc.lower()
 # Check if any keywords appear in the document
 if any(keyword in doc_lower for keyword in keywords):
 relevant_docs.append(doc)

 # If no specific matches, return first few documents
 if not relevant_docs:
 relevant_docs = documents[:3]

 return relevant_docs[:5] # Limit to 5 most relevant documents

 def refresh_cache(self):
 """Clear cached documents to force reload"""
 self._cached_documents = None
