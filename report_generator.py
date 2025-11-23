import pandas as pd
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch

class ReportGenerator:
    def __init__(self, db):
        self.db = db
    
    def gerar_planilha_dia(self, data, filename):
        """Gera planilha Excel para um dia específico"""
        dados = self.db.get_leituras_por_dia(data)
        
        if not dados:
            return False
        
        df = pd.DataFrame(dados, columns=['Código', 'Descrição', 'Data/Hora'])
        df['Data/Hora'] = pd.to_datetime(df['Data/Hora']).dt.strftime('%d/%m/%Y %H:%M:%S')
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=f'Leituras_{data}', index=False)
        
        return True
    
    def gerar_planilha_mes(self, ano, mes, filename):
        """Gera planilha Excel para um mês específico"""
        dados = self.db.get_leituras_por_mes(ano, mes)
        
        if not dados:
            return False
        
        df = pd.DataFrame(dados, columns=['Código', 'Descrição', 'Data/Hora'])
        df['Data/Hora'] = pd.to_datetime(df['Data/Hora']).dt.strftime('%d/%m/%Y %H:%M:%S')
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=f'Leituras_{mes:02d}_{ano}', index=False)
        
        return True
    
    def gerar_pdf_dia(self, data, filename):
        """Gera PDF para um dia específico"""
        dados = self.db.get_leituras_por_dia(data)
        
        if not dados:
            return False
        
        doc = SimpleDocTemplate(filename, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Título
        title = Paragraph(f"Relatório de Leituras - {data}", styles['Title'])
        story.append(title)
        story.append(Spacer(1, 0.2*inch))
        
        # Tabela
        table_data = [['Código de Barras', 'Descrição', 'Data/Hora']]
        for row in dados:
            dt = datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S.%f')
            table_data.append([row[0], row[1] or 'Sem descrição', dt.strftime('%d/%m/%Y %H:%M:%S')])
        
        table = Table(table_data, colWidths=[2*inch, 2.5*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(table)
        doc.build(story)
        return True
    
    def gerar_pdf_mes(self, ano, mes, filename):
        """Gera PDF para um mês específico"""
        dados = self.db.get_leituras_por_mes(ano, mes)
        
        if not dados:
            return False
        
        doc = SimpleDocTemplate(filename, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Título
        title = Paragraph(f"Relatório de Leituras - {mes:02d}/{ano}", styles['Title'])
        story.append(title)
        story.append(Spacer(1, 0.2*inch))
        
        # Tabela
        table_data = [['Código de Barras', 'Descrição', 'Data/Hora']]
        for row in dados:
            dt = datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S.%f')
            table_data.append([row[0], row[1] or 'Sem descrição', dt.strftime('%d/%m/%Y %H:%M:%S')])
        
        table = Table(table_data, colWidths=[2*inch, 2.5*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(table)
        doc.build(story)
        return True