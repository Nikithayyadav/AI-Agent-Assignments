import streamlit as st

st.set_page_config(page_title="Developer Assistant Agent", page_icon="💻", layout="wide")

st.title("💻 AI Developer Assistant Agent")
st.write("Advanced coding workflow assistant for debugging, documentation, testing, and optimization.")

uploaded = st.file_uploader("Upload Python File", type=["py"])

if uploaded:

    code = uploaded.read().decode("utf-8")

    lines = code.split("\n")
    total_lines = len(lines)
    functions = code.count("def ")
    imports = code.count("import ")
    classes = code.count("class ")

    issues = []

    if "except:" in code:
        issues.append("Use specific exceptions instead of bare except.")

    if "while True" in code:
        issues.append("Possible infinite loop detected.")

    if "global " in code:
        issues.append("Avoid global variables.")

    if total_lines > 150:
        issues.append("Large file. Consider splitting modules.")

    if "print(" not in code:
        issues.append("No output/logging statements found.")

    score = 10 - len(issues)
    if score < 1:
        score = 1

    # METRICS
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Lines", total_lines)
    c2.metric("Functions", functions)
    c3.metric("Imports", imports)
    c4.metric("Quality Score", f"{score}/10")

    st.markdown("---")

    # CODE PREVIEW
    st.subheader("📄 Uploaded Code")
    st.code(code, language="python")

    # CODE UNDERSTANDING
    st.subheader("🧠 Code Understanding")

    if functions > 0:
        st.write("This file contains reusable functions.")
    else:
        st.write("No functions detected. Consider modular design.")

    if classes > 0:
        st.write("Object-oriented structure detected.")

    if imports > 0:
        st.write("External libraries/modules are used.")

    # DEBUGGING
    st.subheader("🐞 Debugging Report")

    if issues:
        for i in issues:
            st.warning(i)
    else:
        st.success("No major issues detected.")

    # DOCUMENTATION
    st.subheader("📝 Auto Documentation")

    st.write("This Python module appears to automate or process logic defined in the uploaded file.")
    st.code('''"""
Module Description:
Performs core operations defined by user code.
Recommended to document each function clearly.
"""''')

    # TESTING
    st.subheader("🧪 Suggested Unit Test")

    st.code('''import unittest

class TestModule(unittest.TestCase):

    def test_sample(self):
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()
''', language="python")

    # REFACTOR
    st.subheader("⚙️ Optimization Suggestions")

    st.info("Break repeated logic into functions.")
    st.info("Use logging instead of print for production.")
    st.info("Handle exceptions specifically.")
    st.info("Add comments and docstrings.")

    # DOWNLOAD REPORT
    report = f"""
Developer Assistant Report

Lines: {total_lines}
Functions: {functions}
Imports: {imports}
Quality Score: {score}/10

Issues:
{chr(10).join(issues)}

Suggestions:
- Modularize code
- Improve documentation
- Add tests
"""

    st.download_button(
        "📄 Download Analysis Report",
        report,
        file_name="developer_report.txt"
    )