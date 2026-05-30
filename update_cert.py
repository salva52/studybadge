import json

json_path = "/home/salva-pc/frappe-bench/apps/lms/lms/lms/print_format/certificate/certificate.json"

html = """{% set member = frappe.db.get_value("User", doc.member, ["full_name"], as_dict=True) %}
{% set course = frappe.db.get_value("LMS Course", doc.course, ["title", "name", "image"], as_dict=True) %}
{% set logo = frappe.db.get_single_value("Website Settings", "banner_image") %}
{% set brand_name = frappe.db.get_single_value("Website Settings", "app_name") %}
{% set instructors = frappe.get_all("Course Instructor", {"parent": doc.course}, pluck="instructor", order_by="idx") %}

<meta name="pdfkit-orientation" content="Landscape">
<meta name="pdfkit-margin-top" content="0">
<meta name="pdfkit-margin-bottom" content="0">
<meta name="pdfkit-margin-left" content="0">
<meta name="pdfkit-margin-right" content="0">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;800&family=Playfair+Display:ital,wght@0,600;1,700&display=swap" rel="stylesheet">

<div class="certificate-wrapper">
    <div class="certificate-inner">
        <!-- Header / Logo -->
        <div class="cert-header">
            <img src="/assets/lms/images/studybadge/studybadge-logo.png" class="cert-logo">
        </div>

        <!-- Title -->
        <div class="cert-title">
            CERTIFICADO DE FINALIZACIÓN
        </div>
        
        <div class="cert-subtitle">
            Se otorga el presente certificado a:
        </div>

        <!-- Student Name -->
        <div class="cert-name">
            {{ member.full_name }}
        </div>

        <!-- Course Details -->
        <div class="cert-body">
            Por haber completado satisfactoriamente el curso<br>
            <span class="cert-course">{{ course.title }}</span><br>
            incluyendo todas las evaluaciones requeridas, el día <span class="cert-date">{{ frappe.utils.format_date(doc.issue_date, "long") }}</span>.
        </div>

        <!-- Footer / Signatures -->
        <div class="cert-footer">
            <table style="width: 100%;">
                <tr>
                    <td style="width: 33%; text-align: center; vertical-align: bottom;">
                        <div class="signature-line"></div>
                        <div class="signature-title">
                            {% if doc.evaluator %}
                                {{ doc.evaluator_name }}<br>
                                <span style="font-size: 0.8em; font-weight: 400;">Evaluador Principal</span>
                            {% else %}
                                {% for instructor in instructors %}
                                    {% set instructor_name = frappe.db.get_value("User", instructor, "full_name") %}
                                    {{ instructor_name }}{% if not loop.last %}, {% endif %}
                                {% endfor %}
                                <br>
                                <span style="font-size: 0.8em; font-weight: 400;">Instructor(es)</span>
                            {% endif %}
                        </div>
                    </td>
                    <td style="width: 33%; text-align: center;">
                        <div class="cert-badge">
                            <div class="badge-inner">
                                <span style="display:block; font-size:12px; margin-top: 18px;">SELLO DE</span>
                                <span style="display:block; font-size:10px; margin-top: 3px;">EXCELENCIA</span>
                            </div>
                        </div>
                    </td>
                    <td style="width: 33%; text-align: center; vertical-align: bottom;">
                        <div class="signature-line"></div>
                        <div class="signature-title">
                            {{ brand_name }}<br>
                            <span style="font-size: 0.8em; font-weight: 400;">Dirección Académica</span>
                        </div>
                    </td>
                </tr>
            </table>
        </div>
    </div>
</div>
"""

css = """
body {
    margin: 0;
    padding: 0;
    background-color: #ffffff;
}

.certificate-wrapper {
    width: 100%;
    min-height: 700px;
    box-sizing: border-box;
    padding: 30px;
    background-color: #ffffff;
    border: 15px solid #1e3a8a;
    position: relative;
    font-family: 'Montserrat', sans-serif;
}

.certificate-inner {
    border: 3px solid #d97706;
    padding: 40px;
    min-height: 600px;
    box-sizing: border-box;
    position: relative;
    text-align: center;
    background-color: #f8fafc;
}

.cert-header {
    margin-top: 10px;
    margin-bottom: 30px;
}

.cert-logo {
    max-height: 60px;
}

.cert-brand {
    font-size: 28px;
    font-weight: 800;
    color: #1e3a8a;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.cert-title {
    font-size: 38px;
    font-weight: 800;
    color: #1e3a8a;
    letter-spacing: 4px;
    margin-bottom: 20px;
}

.cert-subtitle {
    font-size: 16px;
    color: #4b5563;
    margin-bottom: 20px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.cert-name {
    font-family: 'Playfair Display', serif;
    font-size: 52px;
    font-style: italic;
    color: #1e40af;
    margin-bottom: 30px;
    border-bottom: 2px solid #d97706;
    display: inline-block;
    padding-bottom: 10px;
    min-width: 60%;
}

.cert-body {
    font-size: 18px;
    color: #374151;
    line-height: 1.6;
    margin-bottom: 40px;
    width: 80%;
    margin-left: auto;
    margin-right: auto;
}

.cert-course {
    display: block;
    font-size: 26px;
    font-weight: 600;
    color: #1e3a8a;
    margin: 10px 0;
}

.cert-date {
    font-weight: 600;
    color: #111827;
}

.cert-footer {
    margin-top: 40px;
    width: 100%;
}

.signature-line {
    border-top: 1px solid #9ca3af;
    width: 80%;
    margin: 0 auto 10px auto;
}

.signature-title {
    font-size: 14px;
    font-weight: 600;
    color: #4b5563;
}

.cert-badge {
    width: 90px;
    height: 90px;
    background-color: #d97706;
    border-radius: 50%;
    margin: 0 auto;
    position: relative;
    border: 3px solid #fcd34d;
}

.badge-inner {
    width: 76px;
    height: 76px;
    background-color: #1e3a8a;
    border-radius: 50%;
    position: absolute;
    top: 4px;
    left: 4px;
    color: white;
    font-family: 'Montserrat', sans-serif;
    text-align: center;
}
"""

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

data['html'] = html
data['css'] = css

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=1)

print("Certificate successfully updated.")
