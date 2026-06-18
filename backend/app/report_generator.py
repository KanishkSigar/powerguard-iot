import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet

def generate_monthly_report_pdf(month_str: str, channel: str, data: dict) -> io.BytesIO:
    """
    Generate a monthly PDF report using ReportLab.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
    
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    normal_style = styles['Normal']
    
    elements = []
    
    # Title
    elements.append(Paragraph("PowerGuard IoT - Monthly Energy Report", title_style))
    elements.append(Paragraph(f"Month: {month_str} | Channel: {channel}", normal_style))
    elements.append(Spacer(1, 20))
    
    # Summary Info
    elements.append(Paragraph(f"<b>Total Energy Consumed:</b> {data.get('total_kwh', 0)} kWh", normal_style))
    elements.append(Paragraph(f"<b>Estimated Cost:</b> ₹ {data.get('cost_inr', 0)}", normal_style))
    elements.append(Paragraph(f"<b>Average Daily Consumption:</b> {data.get('avg_daily_kwh', 0)} kWh", normal_style))
    elements.append(Spacer(1, 20))
    
    # Daily Breakdown Table
    table_data = [["Date", "Avg Power (W)", "Energy (kWh)", "Cost (INR)"]]
    for day in data.get("daily_breakdown", []):
        table_data.append([
            day.get("date", ""),
            str(day.get("avg_power_watts", 0)),
            str(day.get("total_kwh", 0)),
            str(day.get("cost_inr", 0))
        ])
    
    if len(table_data) > 1:
        t = Table(table_data, colWidths=[120, 100, 100, 100])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4f46e5")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#f8fafc")),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#e2e8f0"))
        ]))
        elements.append(t)
    else:
        elements.append(Paragraph("No daily breakdown data available for this month.", normal_style))
        
    doc.build(elements)
    buffer.seek(0)
    return buffer
