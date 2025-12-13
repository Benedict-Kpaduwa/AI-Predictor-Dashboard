from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
from typing import List, Dict
import io

class MaintenanceReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#000000'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#000000'),
            spaceAfter=12,
            spaceBefore=12
        )
    
    def generate_report(self, assets: List[Dict], summary: Dict) -> bytes:
        """Generate PDF report from assets data"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch)
        story = []

        title = Paragraph("AI Maintenance Predictor Report", self.title_style)
        story.append(title)
        story.append(Spacer(1, 0.2*inch))

        meta_style = self.styles['Normal']
        date_text = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        story.append(Paragraph(date_text, meta_style))
        story.append(Spacer(1, 0.3*inch))

        story.append(Paragraph("Executive Summary", self.heading_style))
        summary_data = [
            ['Metric', 'Value'],
            ['Total Assets', str(summary['total_assets'])],
            ['Healthy', f"{summary['healthy']} ({summary['healthy']/summary['total_assets']*100:.1f}%)"],
            ['Warning', f"{summary['warning']} ({summary['warning']/summary['total_assets']*100:.1f}%)"],
            ['Critical', f"{summary['critical']} ({summary['critical']/summary['total_assets']*100:.1f}%)"],
            ['Average Risk Score', f"{summary['avg_risk_score']:.2f}%"]
        ]
        
        summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#000000')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        
        story.append(summary_table)
        story.append(Spacer(1, 0.4*inch))

        critical_assets = [a for a in assets if a['riskLevel'] == 'critical']
        if critical_assets:
            story.append(Paragraph(f"⚠️ Critical Assets Requiring Immediate Attention ({len(critical_assets)})", self.heading_style))
            for asset in critical_assets[:5]:  # Top 5 critical
                story.append(self._create_asset_paragraph(asset, colors.red))
            story.append(Spacer(1, 0.2*inch))
        
        warning_assets = [a for a in assets if a['riskLevel'] == 'warning']
        if warning_assets:
            story.append(Paragraph(f"⚡ Warning Assets ({len(warning_assets)})", self.heading_style))
            for asset in warning_assets[:5]:  # Top 5 warning
                story.append(self._create_asset_paragraph(asset, colors.orange))
            story.append(Spacer(1, 0.2*inch))
        
        story.append(PageBreak())
        story.append(Paragraph("Detailed Asset Analysis", self.heading_style))
        
        table_data = [['Asset', 'Risk', 'Temp (°C)', 'Vib (mm/s)', 'Pressure (PSI)', 'Days to Failure']]
        
        for asset in sorted(assets, key=lambda x: x['riskScore'], reverse=True):
            row = [
                asset['name'],
                f"{asset['riskScore']:.1f}%",
                f"{asset['temperature']:.1f}",
                f"{asset['vibration']:.2f}",
                f"{asset['pressure']:.1f}",
                str(asset['predictedFailure'])
            ]
            table_data.append(row)
        
        detail_table = Table(table_data, colWidths=[1.5*inch, 0.8*inch, 0.9*inch, 0.9*inch, 1*inch, 1*inch])
        detail_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#000000')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        
        for idx, asset in enumerate(sorted(assets, key=lambda x: x['riskScore'], reverse=True), start=1):
            if asset['riskLevel'] == 'critical':
                detail_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, idx), (-1, idx), colors.HexColor('#fee2e2'))
                ]))
            elif asset['riskLevel'] == 'warning':
                detail_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, idx), (-1, idx), colors.HexColor('#fef3c7'))
                ]))
        
        story.append(detail_table)
        story.append(Spacer(1, 0.3*inch))
        
        story.append(PageBreak())
        story.append(Paragraph("AI-Powered Recommendations", self.heading_style))
        
        recommendations = self._generate_recommendations(assets, summary)
        for i, rec in enumerate(recommendations, 1):
            rec_text = f"<b>{i}.</b> {rec}"
            story.append(Paragraph(rec_text, self.styles['Normal']))
            story.append(Spacer(1, 0.1*inch))
        
        # Footer
        story.append(Spacer(1, 0.5*inch))
        footer_text = "<i>Generated by AI Maintenance Predictor | Powered by Machine Learning</i>"
        footer_style = ParagraphStyle('Footer', parent=self.styles['Normal'], 
                                       fontSize=8, textColor=colors.grey, alignment=TA_CENTER)
        story.append(Paragraph(footer_text, footer_style))
        
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
    
    def _create_asset_paragraph(self, asset: Dict, color) -> Paragraph:
        """Create a formatted paragraph for an asset"""
        text = f"""
        <b>{asset['name']}</b> - Risk: {asset['riskScore']:.1f}%<br/>
        Temperature: {asset['temperature']:.1f}°C | 
        Vibration: {asset['vibration']:.2f} mm/s | 
        Pressure: {asset['pressure']:.1f} PSI<br/>
        <i>Predicted failure in {asset['predictedFailure']} days</i>
        """
        style = ParagraphStyle('AssetStyle', parent=self.styles['Normal'], 
                               leftIndent=20, spaceAfter=10)
        return Paragraph(text, style)
    
    def _generate_recommendations(self, assets: List[Dict], summary: Dict) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        critical_count = summary['critical']
        warning_count = summary['warning']
        
        if critical_count > 0:
            recommendations.append(
                f"<b>Immediate Action Required:</b> {critical_count} asset(s) are in critical condition. "
                "Schedule emergency maintenance inspections within 24 hours."
            )
        
        if warning_count > 0:
            recommendations.append(
                f"<b>Preventive Maintenance:</b> {warning_count} asset(s) showing warning signs. "
                "Plan maintenance within the next 7 days to prevent failures."
            )
        
        high_temp = [a for a in assets if a['temperature'] > 85]
        if high_temp:
            recommendations.append(
                f"<b>Temperature Alert:</b> {len(high_temp)} asset(s) operating above normal temperature. "
                "Check cooling systems and lubrication schedules."
            )
        
        high_vib = [a for a in assets if a['vibration'] > 2.0]
        if high_vib:
            recommendations.append(
                f"<b>Vibration Alert:</b> {len(high_vib)} asset(s) showing elevated vibration levels. "
                "Inspect bearings, alignment, and mounting systems."
            )
        
        high_runtime = [a for a in assets if a['runtime'] > 4500]
        if high_runtime:
            recommendations.append(
                f"<b>Runtime Review:</b> {len(high_runtime)} asset(s) have exceeded 4500 hours. "
                "Consider scheduled downtime for comprehensive inspection."
            )
        
        if summary['healthy'] == summary['total_assets']:
            recommendations.append(
                "<b>Fleet Health:</b> All assets operating within normal parameters. "
                "Continue routine monitoring and preventive maintenance schedule."
            )
        
        recommendations.append(
            "<b>Data Quality:</b> Ensure sensor calibration is current. "
            "Validate readings monthly to maintain prediction accuracy."
        )
        
        return recommendations