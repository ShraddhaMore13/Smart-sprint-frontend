# robust_document_processor.py
import re
import docx
import csv
import os
import zipfile
import xml.etree.ElementTree as ET
from nlp_pipeline import NLPPipeline

class RobustDocumentProcessor:
    def __init__(self):
        self.nlp = NLPPipeline()
    
    def extract_text_from_docx(self, doc_path):
        """Extract text from a .docx file using multiple methods"""
        # Method 1: Try using python-docx
        try:
            doc = docx.Document(doc_path)
            paragraphs = []
            for para in doc.paragraphs:
                paragraphs.append(para.text)
            return '\n'.join(paragraphs)
        except:
            pass
        
        # Method 2: Try using zipfile to extract document.xml
        try:
            with zipfile.ZipFile(doc_path) as zf:
                document_xml = zf.read('word/document.xml')
            
            root = ET.fromstring(document_xml)
            
            # Extract text from XML
            namespaces = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            text_nodes = root.findall('.//w:t', namespaces)
            
            text_parts = []
            for node in text_nodes:
                if node.text:
                    text_parts.append(node.text)
            
            return ''.join(text_parts)
        except:
            pass
        
        # Method 3: Try using zipfile with different XML paths
        try:
            with zipfile.ZipFile(doc_path) as zf:
                # List all files to find the document
                for name in zf.namelist():
                    if 'document' in name and name.endswith('.xml'):
                        document_xml = zf.read(name)
                        root = ET.fromstring(document_xml)
                        
                        namespaces = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
                        text_nodes = root.findall('.//w:t', namespaces)
                        
                        text_parts = []
                        for node in text_nodes:
                            if node.text:
                                text_parts.append(node.text)
                        
                        return ''.join(text_parts)
        except:
            pass
        
        # If all methods fail, raise an exception
        raise Exception(f"Could not extract text from {doc_path}")
    
    def process_document(self, doc_path):
        """Process a document and extract multiple tasks"""
        try:
            # Check if file exists
            if not os.path.exists(doc_path):
                raise FileNotFoundError(f"File not found: {doc_path}")
            
            # Check file extension
            file_ext = os.path.splitext(doc_path)[1].lower()
            
            # Extract text based on file type
            if file_ext == '.docx':
                document_text = self.extract_text_from_docx(doc_path)
            elif file_ext == '.txt':
                with open(doc_path, 'r', encoding='utf-8') as file:
                    document_text = file.read()
            else:
                raise ValueError(f"Unsupported file format: {file_ext}. Please use .docx or .txt format.")
            
            print(f"Extracted text length: {len(document_text)} characters")
            print(f"Text preview: {document_text[:200]}...")
            
            # Split the document into tasks using regex
            task_pattern = r'Task\s+\d+[:\s]*(.*?)(?=Task\s+\d+[:\s]*|$)'
            matches = re.findall(task_pattern, document_text, re.DOTALL)
            
            print(f"Found {len(matches)} tasks in document")
            
            tasks = []
            for i, match in enumerate(matches):
                # Each match is the content of one task
                task_text = match.strip()
                
                # Extract title: the first line of the task_text might be the title
                lines = task_text.split('\n')
                title = lines[0].strip()
                # The rest is the description
                description = '\n'.join(lines[1:]).strip()
                
                # If the title is empty, generate one
                if not title:
                    title = f"Task {i+1}"
                
                # Extract priority from the task_text
                priority_match = re.search(r'Priority:\s*(high|medium|low)', task_text, re.IGNORECASE)
                priority = priority_match.group(1).lower() if priority_match else 'medium'
                
                # Estimate hours based on complexity of the task description
                complexity = self.nlp.analyze_complexity(description)
                estimated_hours = complexity * 8  # Simple heuristic
                
                tasks.append({
                    'title': title,
                    'description': description,
                    'priority': priority,
                    'estimated_hours': estimated_hours
                })
                
                print(f"Processed task: {title} (Priority: {priority}, Hours: {estimated_hours})")
            
            return tasks
        
        except Exception as e:
            # Re-raise the exception with more context
            raise Exception(f"Error processing document {doc_path}: {str(e)}")
    
    def create_text_backup(self, doc_path):
        """Create a text backup of the document"""
        try:
            file_ext = os.path.splitext(doc_path)[1].lower()
            txt_path = os.path.splitext(doc_path)[0] + '_backup.txt'
            
            if file_ext == '.docx':
                document_text = self.extract_text_from_docx(doc_path)
            elif file_ext == '.txt':
                with open(doc_path, 'r', encoding='utf-8') as file:
                    document_text = file.read()
            else:
                return None
            
            with open(txt_path, 'w', encoding='utf-8') as file:
                file.write(document_text)
            
            print(f"Created text backup: {txt_path}")
            return txt_path
        except Exception as e:
            print(f"Could not create text backup: {e}")
            return None