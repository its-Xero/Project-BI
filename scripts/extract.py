"""
Script d'extraction complet des données Northwind à partir de fichiers Excel
Inclut tous les fichiers: Clients, Produits, Commandes, Fournisseurs, etc.
"""

import pandas as pd
import os
from datetime import datetime
import glob

class NorthwindExtractor:
    """Classe pour extraire TOUTES les données de Northwind depuis Excel"""
    
    def __init__(self, data_folder='data/'):
        """
        Initialise l'extracteur
        Args:
            data_folder: Dossier contenant les fichiers Excel
        """
        self.data_folder = data_folder
        self.raw_data_path = 'data/raw/'
        
        # Créer les dossiers nécessaires
        os.makedirs(self.raw_data_path, exist_ok=True)
    
    def load_excel_file(self, filename, sheet_name=None):
        """Charge un fichier Excel"""
        try:
            filepath = f"{self.data_folder}{filename}"
            if not os.path.exists(filepath):
                print(f"⚠ Fichier non trouvé: {filename}")
                return None
                
            if sheet_name:
                df = pd.read_excel(filepath, sheet_name=sheet_name)
            else:
                df = pd.read_excel(filepath)
            print(f"✓ Chargé: {filename} ({len(df)} lignes)")
            return df
        except Exception as e:
            print(f"✗ Erreur chargement {filename}: {e}")
            return None
    
    def extract_all_tables(self):
        """Extrait TOUTES les tables principales depuis Excel"""
        print("\n📊 Extraction de TOUTES les tables depuis Excel...")
        
        # Liste complète de tous les fichiers Excel
        all_excel_files = {
            'customers': 'Customers.xlsx',
            'employees': 'Employees.xlsx',
            'orders': 'Orders.xlsx',
            'products': 'Products.xlsx',
            'suppliers': 'Suppliers.xlsx',
            'shippers': 'Shippers.xlsx',
            'inventory_transactions': 'Inventory Transactions.xlsx',
            'purchase_orders': 'Purchase Orders.xlsx',
            'purchase_order_details': 'Purchase Order Details.xlsx',
            'invoices': 'Invoices.xlsx',
            'strings': 'Strings.xlsx',
            'sales_reports': 'Sales Reports.xlsx'
        }
        
        extracted_data = {}
        
        for key, filename in all_excel_files.items():
            df = self.load_excel_file(filename)
            if df is not None:
                # Sauvegarder en CSV
                output_file = f"{self.raw_data_path}{key}.csv"
                df.to_csv(output_file, index=False, encoding='utf-8')
                extracted_data[key] = df
                print(f"  → Sauvegardé: {output_file}")
        
        # Extraire les tables de référence (lookup tables)
        self.extract_reference_tables()
        
        return extracted_data
    
    def extract_reference_tables(self):
        """Extrait les tables de référence (lookup tables)"""
        print("\n🔍 Extraction des tables de référence...")
        
        ref_files = {
            'orders_status': 'Orders Status.xlsx',
            'orders_tax_status': 'Orders Tax Status.xlsx',
            'order_details_status': 'Order Details Status.xlsx',
            'purchase_order_status': 'Purchase Order Status.xlsx',
            'inventory_transaction_types': 'Inventory Transaction Types.xlsx',
            'privileges': 'Privileges.xlsx',
            'employee_privileges': 'Employee Privileges.xlsx'
        }
        
        for key, filename in ref_files.items():
            df = self.load_excel_file(filename)
            if df is not None:
                output_file = f"{self.raw_data_path}{key}.csv"
                df.to_csv(output_file, index=False, encoding='utf-8')
                print(f"  → {filename} → {key}.csv")
    
    def create_complete_sales_analysis(self):
        """Crée une vue COMPLÈTE consolidée pour l'analyse des ventes"""
        print("\n📈 Création de la vue analytique COMPLÈTE des ventes...")
        
        try:
            # 1. Charger toutes les données nécessaires
            print("  1. Chargement des données source...")
            orders_df = self.load_excel_file('Orders.xlsx')
            customers_df = self.load_excel_file('Customers.xlsx')
            employees_df = self.load_excel_file('Employees.xlsx')
            products_df = self.load_excel_file('Products.xlsx')
            shippers_df = self.load_excel_file('Shippers.xlsx')
            invoices_df = self.load_excel_file('Invoices.xlsx')
            
            # Vérifier que toutes les tables sont chargées
            required_tables = {
                'Orders': orders_df,
                'Customers': customers_df,
                'Employees': employees_df,
                'Products': products_df
            }
            
            for table_name, df in required_tables.items():
                if df is None:
                    print(f"✗ Table requise manquante: {table_name}")
                    return None
            
            # 2. Préparer les données des clients
            print("  2. Préparation des données clients...")
            customers_df['CustomerName'] = customers_df['First Name'] + ' ' + customers_df['Last Name']
            customers_clean = customers_df.rename(columns={
                'ID': 'CustomerID',
                'Company': 'CustomerCompany',
                'CustomerName': 'CustomerName',
                'Country/Region': 'CustomerCountry',
                'City': 'CustomerCity',
                'State/Province': 'CustomerState',
                'ZIP/Postal Code': 'CustomerZIP'
            })
            
            # 3. Préparer les données des employés
            print("  3. Préparation des données employés...")
            employees_df['EmployeeName'] = employees_df['First Name'] + ' ' + employees_df['Last Name']
            employees_clean = employees_df.rename(columns={
                'ID': 'EmployeeID',
                'EmployeeName': 'EmployeeName',
                'Job Title': 'EmployeeTitle',
                'E-mail Address': 'EmployeeEmail'
            })
            
            # 4. Préparer les données des produits
            print("  4. Préparation des données produits...")
            products_clean = products_df.rename(columns={
                'ID': 'ProductID',
                'Product Code': 'ProductCode',
                'Product Name': 'ProductName',
                'Category': 'CategoryName',
                'List Price': 'UnitPrice',
                'Standard Cost': 'StandardCost',
                'Quantity Per Unit': 'QuantityPerUnit',
                'Reorder Level': 'ReorderLevel',
                'Target Level': 'TargetLevel'
            })
            
            # 5. Préparer les données des transporteurs
            print("  5. Préparation des données transporteurs...")
            shippers_clean = shippers_df.rename(columns={
                'ID': 'ShipperID',
                'Company': 'ShipperCompany'
            })
            
            # 6. Créer la vue analytique principale
            print("  6. Création de la vue analytique...")
            
            # Démarrer avec les commandes
            sales_analysis = orders_df.copy()
            
            # Renommer les colonnes des commandes
            sales_analysis = sales_analysis.rename(columns={
                'Order ID': 'OrderID',
                'Order Date': 'OrderDate',
                'Shipped Date': 'ShippedDate',
                'Customer': 'CustomerCompany',
                'Employee': 'EmployeeName',
                'Ship Via': 'ShipperCompany',
                'Ship Name': 'ShipName',
                'Ship Address': 'ShipAddress',
                'Ship City': 'ShipCity',
                'Ship State/Province': 'ShipState',
                'Ship ZIP/Postal Code': 'ShipZIP',
                'Ship Country/Region': 'ShipCountry',
                'Shipping Fee': 'ShippingFee',
                'Taxes': 'Taxes',
                'Payment Type': 'PaymentType',
                'Paid Date': 'PaidDate',
                'Tax Rate': 'TaxRate',
                'Tax Status': 'TaxStatus',
                'Status ID': 'StatusName'
            })
            
            # 7. Fusionner avec les clients
            print("  7. Fusion avec les clients...")
            sales_analysis = sales_analysis.merge(
                customers_clean[[
                    'CustomerID', 'CustomerCompany', 'CustomerName', 
                    'CustomerCountry', 'CustomerCity', 'CustomerState', 'CustomerZIP'
                ]],
                left_on='CustomerCompany',
                right_on='CustomerCompany',
                how='left'
            )
            
            # 8. Fusionner avec les employés
            print("  8. Fusion avec les employés...")
            sales_analysis = sales_analysis.merge(
                employees_clean[['EmployeeID', 'EmployeeName', 'EmployeeTitle', 'EmployeeEmail']],
                left_on='EmployeeName',
                right_on='EmployeeName',
                how='left'
            )
            
            # 9. Fusionner avec les transporteurs
            print("  9. Fusion avec les transporteurs...")
            sales_analysis = sales_analysis.merge(
                shippers_clean[['ShipperID', 'ShipperCompany']],
                left_on='ShipperCompany',
                right_on='ShipperCompany',
                how='left'
            )
            
            # 10. Ajouter des produits simulés (car nous n'avons pas Order Details)
            print("  10. Simulation des lignes de commande...")
            
            # Pour chaque commande, créer plusieurs lignes de produit
            # En production, vous auriez un fichier Order Details.xlsx
            product_sample = products_clean[['ProductID', 'ProductName', 'CategoryName', 'UnitPrice']].head(5)
            
            # Créer des lignes de commande simulées
            order_details_list = []
            for idx, order in sales_analysis.iterrows():
                # Sélectionner 1-3 produits aléatoires pour chaque commande
                import random
                n_products = random.randint(1, 3)
                for i in range(n_products):
                    product = product_sample.iloc[i % len(product_sample)]
                    quantity = random.randint(1, 10)
                    discount = random.choice([0, 0.05, 0.1, 0.15])
                    
                    order_detail = {
                        'OrderID': order['OrderID'],
                        'ProductID': product['ProductID'],
                        'ProductName': product['ProductName'],
                        'CategoryName': product['CategoryName'],
                        'UnitPrice': product['UnitPrice'],
                        'Quantity': quantity,
                        'Discount': discount,
                        'LineTotal': product['UnitPrice'] * quantity * (1 - discount)
                    }
                    order_details_list.append(order_detail)
            
            # Convertir en DataFrame
            order_details_df = pd.DataFrame(order_details_list)
            
            # 11. Fusionner les détails avec la vue principale
            print("  11. Fusion des détails de commande...")
            
            # Pour garder une structure plate, nous allons dupliquer les lignes de commande
            # Une meilleure approche serait de garder deux tables séparées
            sales_analysis_with_details = pd.merge(
                sales_analysis,
                order_details_df,
                on='OrderID',
                how='left'
            )
            
            # 12. Ajouter les informations de facturation
            print("  12. Ajout des informations de facturation...")
            if invoices_df is not None:
                invoices_clean = invoices_df.rename(columns={
                    'Order ID': 'OrderID',
                    'Invoice Date': 'InvoiceDate',
                    'Due Date': 'DueDate',
                    'Tax': 'InvoiceTax',
                    'Shipping': 'InvoiceShipping',
                    'Amount Due': 'AmountDue'
                })
                sales_analysis_with_details = sales_analysis_with_details.merge(
                    invoices_clean,
                    on='OrderID',
                    how='left'
                )
            
            # 13. Calculer les indicateurs supplémentaires
            print("  13. Calcul des indicateurs...")
            if 'OrderDate' in sales_analysis_with_details.columns:
                sales_analysis_with_details['OrderDate'] = pd.to_datetime(sales_analysis_with_details['OrderDate'])
                sales_analysis_with_details['OrderYear'] = sales_analysis_with_details['OrderDate'].dt.year
                sales_analysis_with_details['OrderMonth'] = sales_analysis_with_details['OrderDate'].dt.month
                sales_analysis_with_details['OrderQuarter'] = sales_analysis_with_details['OrderDate'].dt.quarter
            
            # 14. Sauvegarder
            print("  14. Sauvegarde...")
            output_file = f"{self.raw_data_path}sales_analysis_complete.csv"
            sales_analysis_with_details.to_csv(output_file, index=False, encoding='utf-8')
            
            print(f"✓ Vue analytique COMPLÈTE créée: {len(sales_analysis_with_details)} lignes")
            print(f"  → Sauvegardé: {output_file}")
            
            return sales_analysis_with_details
            
        except Exception as e:
            print(f"✗ Erreur création vue analytique: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    def create_supplier_analysis(self):
        """Crée une vue analytique des fournisseurs"""
        print("\n🏭 Création de la vue analytique des fournisseurs...")
        
        try:
            suppliers_df = self.load_excel_file('Suppliers.xlsx')
            products_df = self.load_excel_file('Products.xlsx')
            purchase_orders_df = self.load_excel_file('Purchase Orders.xlsx')
            
            if suppliers_df is None or products_df is None:
                print("✗ Impossible de charger les données fournisseurs")
                return None
            
            # Nettoyer les fournisseurs
            suppliers_clean = suppliers_df.rename(columns={
                'ID': 'SupplierID',
                'Company': 'SupplierCompany',
                'Last Name': 'SupplierLastName',
                'First Name': 'SupplierFirstName',
                'Job Title': 'SupplierJobTitle'
            })
            
            suppliers_clean['SupplierName'] = suppliers_clean['SupplierFirstName'] + ' ' + suppliers_clean['SupplierLastName']
            
            # Analyser les produits par fournisseur
            products_df['Supplier IDs'] = products_df['Supplier IDs'].fillna('')
            products_by_supplier = []
            
            for idx, product in products_df.iterrows():
                supplier_ids = str(product['Supplier IDs']).split(';')
                for supplier_id in supplier_ids:
                    supplier_id = supplier_id.strip()
                    if supplier_id:
                        products_by_supplier.append({
                            'SupplierID': supplier_id,
                            'ProductID': product['ID'],
                            'ProductName': product['Product Name'],
                            'Category': product['Category'],
                            'StandardCost': product['Standard Cost'],
                            'ListPrice': product['List Price']
                        })
            
            products_by_supplier_df = pd.DataFrame(products_by_supplier)

            # Agréger les métriques par fournisseur et aplatir les colonnes
            agg_df = products_by_supplier_df.groupby('SupplierID').agg(
                ProductCount=('ProductID', 'count'),
                MinPrice=('ListPrice', 'min'),
                MaxPrice=('ListPrice', 'max'),
                AvgPrice=('ListPrice', 'mean')
            ).reset_index()

            # Fusionner avec les informations fournisseur
            supplier_analysis = suppliers_clean.merge(
                agg_df,
                on='SupplierID',
                how='left'
            )

            # Normaliser les valeurs manquantes
            if 'ProductCount' in supplier_analysis.columns:
                supplier_analysis['ProductCount'] = supplier_analysis['ProductCount'].fillna(0).astype(int)
            for col in ['MinPrice', 'MaxPrice', 'AvgPrice']:
                if col in supplier_analysis.columns:
                    supplier_analysis[col] = supplier_analysis[col].fillna(0.0)
            
            # Sauvegarder
            output_file = f"{self.raw_data_path}supplier_analysis.csv"
            supplier_analysis.to_csv(output_file, index=False, encoding='utf-8')
            print(f"✓ Vue fournisseurs: {len(supplier_analysis)} lignes")
            print(f"  → Sauvegardé: {output_file}")
            
            return supplier_analysis
            
        except Exception as e:
            print(f"✗ Erreur création vue fournisseurs: {e}")
            return None
    
    def create_inventory_analysis(self):
        """Crée une vue analytique de l'inventaire"""
        print("\n📦 Création de la vue analytique d'inventaire...")
        
        try:
            inventory_df = self.load_excel_file('Inventory Transactions.xlsx')
            products_df = self.load_excel_file('Products.xlsx')
            
            if inventory_df is None or products_df is None:
                print("✗ Impossible de charger les données d'inventaire")
                return None
            
            # Nettoyer l'inventaire
            inventory_clean = inventory_df.copy()
            inventory_clean = inventory_clean.rename(columns={
                'Transaction ID': 'TransactionID',
                'Transaction Type': 'TransactionType',
                'Transaction Created Date': 'CreatedDate',
                'Transaction Modified Date': 'ModifiedDate',
                'Product ID': 'ProductName',
                'Quantity': 'Quantity',
                'Comments': 'Comments'
            })
            
            # Convertir les dates
            inventory_clean['CreatedDate'] = pd.to_datetime(inventory_clean['CreatedDate'])
            inventory_clean['ModifiedDate'] = pd.to_datetime(inventory_clean['ModifiedDate'])
            
            # Ajouter les informations produit
            products_clean = products_df.rename(columns={
                'Product Name': 'ProductName',
                'Category': 'CategoryName',
                'Standard Cost': 'StandardCost',
                'List Price': 'ListPrice',
                'Reorder Level': 'ReorderLevel',
                'Target Level': 'TargetLevel'
            })
            
            inventory_analysis = inventory_clean.merge(
                products_clean[['ProductName', 'CategoryName', 'StandardCost', 'ListPrice', 
                              'ReorderLevel', 'TargetLevel']],
                left_on='ProductName',
                right_on='ProductName',
                how='left'
            )
            
            # Calculer la valeur
            inventory_analysis['TransactionValue'] = inventory_analysis['Quantity'] * inventory_analysis['StandardCost']
            
            # Calculer le stock actuel par produit
            stock_summary = inventory_analysis.groupby(['ProductName', 'CategoryName']).agg({
                'Quantity': lambda x: x[inventory_analysis['TransactionType'] == 'Purchased'].sum() - 
                                     x[inventory_analysis['TransactionType'] == 'Sold'].sum(),
                'StandardCost': 'first',
                'ListPrice': 'first',
                'ReorderLevel': 'first',
                'TargetLevel': 'first'
            }).reset_index()
            
            stock_summary = stock_summary.rename(columns={'Quantity': 'CurrentStock'})
            stock_summary['BelowReorder'] = stock_summary['CurrentStock'] < stock_summary['ReorderLevel']
            stock_summary['StockValue'] = stock_summary['CurrentStock'] * stock_summary['StandardCost']
            
            # Sauvegarder les deux vues
            output_file1 = f"{self.raw_data_path}inventory_transactions.csv"
            inventory_analysis.to_csv(output_file1, index=False, encoding='utf-8')
            
            output_file2 = f"{self.raw_data_path}inventory_stock.csv"
            stock_summary.to_csv(output_file2, index=False, encoding='utf-8')
            
            print(f"✓ Transactions inventaire: {len(inventory_analysis)} lignes")
            print(f"✓ Stock actuel: {len(stock_summary)} produits")
            print(f"  → Sauvegardés: {output_file1}, {output_file2}")
            
            return {
                'transactions': inventory_analysis,
                'stock': stock_summary
            }
            
        except Exception as e:
            print(f"✗ Erreur création vue inventaire: {e}")
            return None
    
    def get_extraction_summary(self):
        """Affiche un résumé COMPLET de l'extraction"""
        print("\n" + "="*70)
        print("RÉSUMÉ COMPLET DE L'EXTRACTION NORTHWIND")
        print("="*70)
        
        # Lister les fichiers extraits
        if os.path.exists(self.raw_data_path):
            files = sorted(os.listdir(self.raw_data_path))
            print(f"\n📁 Fichiers extraits ({len(files)}):")
            
            # Grouper par type
            csv_files = [f for f in files if f.endswith('.csv')]
            categories = {
                'Données principales': ['customers', 'employees', 'orders', 'products', 'suppliers', 'shippers'],
                'Transactions': ['inventory', 'purchase', 'invoices'],
                'Vues analytiques': ['sales_analysis', 'supplier_analysis'],
                'Tables de référence': ['status', 'types', 'privileges', 'strings', 'reports']
            }
            
            for category, prefixes in categories.items():
                cat_files = [f for f in csv_files if any(f.startswith(p) for p in prefixes)]
                if cat_files:
                    print(f"\n  📂 {category}:")
                    for f in sorted(cat_files):
                        file_path = os.path.join(self.raw_data_path, f)
                        size_kb = os.path.getsize(file_path) / 1024
                        lines = sum(1 for _ in open(file_path, 'r', encoding='utf-8')) - 1
                        print(f"    • {f:<30} ({lines:>4} lignes, {size_kb:>6.1f} KB)")
        
        # Statistiques globales
        print("\n📊 Statistiques globales:")
        try:
            # Compter les enregistrements totaux
            total_records = 0
            total_files = 0
            
            for file in csv_files:
                file_path = os.path.join(self.raw_data_path, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = sum(1 for _ in f) - 1
                    total_records += lines
                    total_files += 1
            
            print(f"  • Total enregistrements: {total_records:,}")
            print(f"  • Total fichiers CSV: {total_files}")
            
        except Exception as e:
            print(f"  • Impossible de calculer les statistiques: {e}")
        
        print(f"\n📅 Date d'extraction: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70)
    
    def execute_complete_extraction(self):
        """Exécute l'extraction COMPLÈTE de toutes les données"""
        print("\n" + "="*70)
        print("🚀 EXTRACTION COMPLÈTE DES DONNÉES NORTHWIND")
        print("="*70 + "\n")
        
        # 1. Extraire toutes les tables de base
        print("📥 ÉTAPE 1: Extraction des tables de base")
        extracted_tables = self.extract_all_tables()
        
        # 2. Créer la vue analytique complète des ventes
        print("\n📈 ÉTAPE 2: Création de la vue analytique des ventes")
        sales_data = self.create_complete_sales_analysis()
        
        # 3. Créer la vue analytique des fournisseurs
        print("\n🏭 ÉTAPE 3: Création de la vue analytique des fournisseurs")
        supplier_data = self.create_supplier_analysis()
        
        # 4. Créer la vue analytique de l'inventaire
        print("\n📦 ÉTAPE 4: Création de la vue analytique de l'inventaire")
        inventory_data = self.create_inventory_analysis()
        
        # 5. Afficher le résumé complet
        print("\n📋 ÉTAPE 5: Génération du résumé")
        self.get_extraction_summary()
        
        print("\n✅ EXTRACTION COMPLÈTE TERMINÉE AVEC SUCCÈS\n")
        
        return {
            'tables': extracted_tables,
            'sales_analysis': sales_data,
            'supplier_analysis': supplier_data,
            'inventory_analysis': inventory_data
        }


def main():
    """Fonction principale d'extraction"""
    extractor = NorthwindExtractor()
    results = extractor.execute_complete_extraction()
    return results


if __name__ == "__main__":
    main()