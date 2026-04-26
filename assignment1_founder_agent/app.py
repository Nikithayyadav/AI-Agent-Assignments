import streamlit as st
import requests
import time
from ddgs import DDGS

st.set_page_config(page_title="Founder Research Agent", page_icon="🔍", layout="wide")

st.title("🔍 Autonomous Founder / CEO Research Agent")
st.write("Premium multi-source exploration with memory, intelligence, visuals, and executive reporting.")

name = st.text_input("Enter Founder / CEO Name")

if st.button("Start Research"):

    if name:

        progress = st.progress(0)
        status = st.empty()

        memory = []
        sources = []
        image_url = None
        role = "Executive / Founder"

        # STEP 1
        status.info("Searching global sources...")
        progress.progress(20)
        time.sleep(1)

        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(name + " founder CEO company biography", max_results=5))
        except:
            results = []

        # STEP 2
        status.info("Collecting external findings...")
        progress.progress(45)
        time.sleep(1)

        for r in results:
            title = r.get("title", "")
            body = r.get("body", "")
            href = r.get("href", "")

            if title:
                memory.append(title)

            if body:
                memory.append(body)

            if href:
                sources.append(href)

        # WIKIPEDIA ENRICHMENT
        try:
            wiki = f"https://en.wikipedia.org/api/rest_v1/page/summary/{name.replace(' ','_')}"
            res = requests.get(wiki, headers={"User-Agent":"Mozilla/5.0"})

            if res.status_code == 200:
                data = res.json()

                memory.append(data.get("extract", ""))

                if "content_urls" in data:
                    sources.append(data["content_urls"]["desktop"]["page"])

                if "thumbnail" in data:
                    image_url = data["thumbnail"]["source"]

                if "description" in data:
                    role = data["description"]

        except:
            pass

        # STEP 3
        status.info("Building memory intelligence...")
        progress.progress(75)
        time.sleep(1)

        combined = " ".join(memory)

        # Detect Companies
        known = [
            "Tesla", "SpaceX", "Google", "Microsoft",
            "Amazon", "Meta", "PayPal", "xAI", "X",
            "Apple", "OpenAI", "Oracle"
        ]

        companies = []

        for c in known:
            if c.lower() in combined.lower():
                companies.append(c)

        # Dynamic leadership profile
        leadership = "Innovation-driven executive with strong public influence."

        if "Tesla" in companies or "SpaceX" in companies:
            leadership = "High-risk visionary leader focused on disruptive innovation and scaling."

        if "Microsoft" in companies:
            leadership = "Operational and enterprise-focused leadership with long-term strategy."

        if "Google" in companies:
            leadership = "Data-driven product leadership with ecosystem influence."

        # STEP 4
        status.success("Executive report completed.")
        progress.progress(100)

        # HEADER
        col1, col2 = st.columns([1,2])

        with col1:
            if image_url:
                st.image(image_url, width=230)

        with col2:
            st.subheader(name)
            st.write(role)

        # METRICS
        st.markdown("---")

        m1, m2, m3 = st.columns(3)
        m1.metric("Sources Used", len(set(sources)))
        m2.metric("Memory Points", len(memory))
        m3.metric("Confidence", "High" if memory else "Medium")

        # SUMMARY
        st.subheader("📌 Executive Summary")

        if combined:
            st.write(combined[:700] + "...")
        else:
            st.write("No summary available.")

        # COMPANIES
        st.subheader("🏢 Key Companies")

        if companies:
            for c in companies:
                st.write("•", c)
        else:
            st.write("No companies identified.")

        # LEADERSHIP
        st.subheader("🧠 Leadership Profile")
        st.write(leadership)

        # MEMORY
        st.subheader("🗂 Agent Memory")

        for item in memory[:6]:
            st.write("•", item[:150])

        # SOURCES
        st.subheader("🌐 Sources Explored")

        for s in list(set(sources))[:5]:
            st.write(s)

        # DOWNLOAD REPORT
        report = f"""
Founder Research Report

Name: {name}
Role: {role}

Sources Used: {len(set(sources))}
Memory Points: {len(memory)}

Companies:
{', '.join(companies)}

Leadership:
{leadership}

Summary:
{combined[:1500]}
"""

        st.download_button(
            "📄 Download Executive Report",
            report,
            file_name="founder_report.txt"
        )