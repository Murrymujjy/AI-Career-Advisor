import streamlit as st
import requests
from advisor_logic import generate_cover_letter
from fpdf import FPDF
from docx import Document
import os

# Helper: Generate PDF
def generate_pdf_from_text(text, filename="cover_letter.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for line in text.split("\n"):
        pdf.multi_cell(0, 10, line)
    output_path = os.path.join("/tmp", filename)
    pdf.output(output_path)
    return output_path

# Helper: Generate Word (DOCX)
def generate_docx_from_text(text, filename="cover_letter.docx"):
    doc = Document()
    for line in text.strip().split("\n"):
        doc.add_paragraph(line)
    output_path = os.path.join("/tmp", filename)
    doc.save(output_path)
    return output_path

def show():
    st.title("🔍 Job Finder & Auto Apply")
    st.markdown("Search for remote jobs and get a tailored cover letter.")

    with st.form("job_search_form"):
        job_title = st.text_input("Job Title", "Machine Learning Engineer")
        location = st.text_input("Preferred Location (optional)", "")
        keywords = st.text_input("Keywords (comma-separated, optional)", "")
        submit_job_search = st.form_submit_button("Search Jobs")

    if submit_job_search:
        st.info("Searching for jobs...")

        try:
            remotive_url = f"https://remotive.io/api/remote-jobs?search={job_title}"
            res = requests.get(remotive_url)
            jobs = res.json().get("jobs", [])

            if jobs:
                st.success(f"Found {len(jobs)} job(s). Showing top 10.")
                for job in jobs[:10]:
                    with st.expander(f"{job['title']} at {job['company_name']}"):
                        st.write(f"**Location:** {job['candidate_required_location']}")
                        st.write(f"**Category:** {job['category']}")
                        st.write(f"**Published:** {job['publication_date']}")
                        st.write(job['description'][:500] + "...")
                        apply_url = job.get("url")
                        job_desc = job['description'][:1000]

                        # Form for Cover Letter generation
                        with st.form(f"cover_letter_form_{job['id']}"):
                            user_name = st.text_input("Your Name", key=f"name_{job['id']}")
                            user_email = st.text_input("Your Email", key=f"email_{job['id']}")
                            user_background = st.text_area("Your Background", key=f"background_{job['id']}")
                            user_skills = st.text_area("Relevant Skills or Experience", key=f"skills_{job['id']}")
                            tone = st.selectbox("Tone of Cover Letter", ["Professional", "Friendly", "Formal"], key=f"tone_{job['id']}")
                            file_format = st.radio("Download Format", ["PDF", "Word (DOCX)"], key=f"format_{job['id']}")
                            submit_cover = st.form_submit_button("Generate Cover Letter")

                        if submit_cover:
                            if not user_name or not user_email or not user_background or not user_skills:
                                st.warning("⚠️ Please fill in all the fields.")
                            else:
                                with st.spinner("Generating tailored cover letter..."):
                                    try:
                                        cover_letter = generate_cover_letter(
                                            name=user_name,
                                            email=user_email,
                                            role=job['title'],
                                            company=job['company_name'],
                                            job_desc=job_desc,
                                            tone=tone,
                                            language="English"
                                        )
                                        st.success("✅ Cover letter generated!")
                                        st.text_area("📄 Your Cover Letter", value=cover_letter, height=400)

                                        # Download buttons
                                        if file_format == "PDF":
                                            file_path = generate_pdf_from_text(cover_letter, filename=f"{user_name}_cover_letter.pdf")
                                            file_name = f"{user_name}_cover_letter.pdf"
                                            mime_type = "application/pdf"
                                        else:
                                            file_path = generate_docx_from_text(cover_letter, filename=f"{user_name}_cover_letter.docx")
                                            file_name = f"{user_name}_cover_letter.docx"
                                            mime_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

                                        with open(file_path, "rb") as f:
                                            st.download_button(
                                                label=f"📥 Download as {file_format}",
                                                data=f,
                                                file_name=file_name,
                                                mime=mime_type
                                            )

                                        if apply_url:
                                            st.markdown(f"[🌐 Go to Job Page and Apply]({apply_url})", unsafe_allow_html=True)
                                    except Exception as e:
                                        st.error(f"❌ Error generating cover letter: {e}")
            else:
                st.warning("No jobs found for the specified title.")

        except Exception as e:
            st.error(f"❌ Error fetching jobs: {e}")
