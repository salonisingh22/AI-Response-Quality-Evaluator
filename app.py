import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import datetime
import os

from src.orchestrator.orchestrator import evaluate_response


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AI Response Quality Evaluator",
    page_icon="🤖",
    layout="wide"
)


# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

body{
    background:#0E1117;
}


.stApp{
    background:
    radial-gradient(circle at top,#172554,#0E1117 45%);
}


h1{
    text-align:center;
    font-size:48px;
    background:linear-gradient(90deg,#00E5FF,#8B5CF6);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    font-weight:900;
}


h2,h3{
    color:white;
}


p{
    color:#CBD5E1;
}


.block-container{
    padding-top:2rem;
}


.card{

    background:#111827;
    padding:20px;
    border-radius:20px;
    border:1px solid #374151;
    box-shadow:0 0 20px rgba(0,229,255,0.15);

}


.agent-card{

    background:#1F2937;
    padding:15px;
    border-radius:15px;
    margin-bottom:12px;
    border-left:5px solid #00E5FF;

}



div[data-testid="metric-container"]{

    background:#111827;
    padding:20px;
    border-radius:18px;
    border:1px solid #374151;

}



.stButton>button{

    background:linear-gradient(
    90deg,
    #00E5FF,
    #8B5CF6
    );

    color:white;

    font-size:20px;

    font-weight:bold;

    height:60px;

    border-radius:15px;

    border:none;

}



.stButton>button:hover{

    transform:scale(1.02);

}



textarea{

    background:#111827 !important;

    color:white !important;

    border-radius:15px !important;

}



[data-testid="stSidebar"]{

    background:#111827;

}



footer{

visibility:hidden;

}


header{

visibility:hidden;

}



</style>

""", unsafe_allow_html=True)



# ---------------- SIDEBAR ----------------


# ---------------- SIDEBAR ----------------


with st.sidebar:

    st.markdown("# 🤖 AI Evaluator")

    st.success("🟢 System Status")

    st.progress(100)

    st.metric("Version", "2.0")

    st.metric("Architecture", "Multi-Agent")

    st.metric("Agents", "5")

    st.metric("Evaluation", "Real-Time")

    st.markdown("---")


    st.markdown(
    """
    ### 📌 Project Overview

    This system evaluates AI generated
    responses using multiple intelligent
    agents.

    """
    )


    st.markdown("---")


    st.markdown(
    """
    ### 🛠 Technology Stack

    🐍 Python

    ⚡ Streamlit

    🧠 Multi-Agent Architecture

    🔍 NLP Evaluation

    """
    )



# ---------------- HEADER ----------------


st.markdown(
"""
# 🤖 AI Response Quality Evaluator

### Multi-Agent Intelligent Evaluation Platform

Evaluate AI generated answers based on:

🎯 Relevance  
✅ Accuracy  
⚠ Hallucination Detection  
📄 Completeness  

---
"""
)


# ---------------- PROJECT STATISTICS ----------------

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("🤖 Agents", "5")

with c2:
    st.metric("📊 Metrics", "4")

with c3:
    st.metric("⚡ Speed", "Real-Time")

with c4:
    st.metric("🧠 Version", "2.0")

# ---------------- PROJECT INTRO ----------------


with st.container():

    st.markdown(
    """
    <div class="card">

    <h3>🚀 About This Project</h3>

    <p>

    The <b>AI Response Quality Evaluator</b> is an intelligent
    multi-agent system designed to evaluate AI-generated
    responses using four specialized evaluation agents.

    Each agent independently measures one quality parameter,
    and the Verdict Agent combines all individual scores to
    produce an overall response quality score.

    </p>

    </div>
    """,
    unsafe_allow_html=True
    )


st.write("")


# ---------------- MAIN AREA ----------------



# ---------------- MAIN AREA ----------------


left,right = st.columns([2,1])



with left:


    st.subheader("📥 Input Data")


    question = st.text_area(

        "📝 User Question",

        placeholder="Enter user query here...",

        height=120

    )


    ai_response = st.text_area(

        "🤖 AI Generated Response",

        placeholder="Paste AI response here...",

        height=220

    )


    reference = st.text_area(

        "📚 Reference Answer",

        placeholder="Optional reference answer...",

        height=180

    )


    evaluate = st.button(
        "🚀 Run AI Evaluation",
        use_container_width=True
    )



with right:


    st.markdown(
    """

    <div class="card">

    <h3>🧠 Evaluation Agents</h3>

    </div>

    """,
    unsafe_allow_html=True
    )


    agents=[

    ("🎯 Relevance Agent",
    "Checks whether response answers the user query."),


    ("✅ Accuracy Agent",
    "Checks correctness of information."),


    ("⚠ Hallucination Agent",
    "Detects unsupported information."),


    ("📄 Completeness Agent",
    "Checks missing important points."),


    ("🏆 Verdict Agent",
    "Generates final quality score.")

    ]


    for name,desc in agents:

        st.markdown(

        f"""

        <div class="agent-card">

        <b>{name}</b>

        <br>

        <small>{desc}</small>

        </div>

        """,

        unsafe_allow_html=True

        )



# ---------------- RESULTS ----------------

if evaluate:

    if question.strip() == "" or ai_response.strip() == "":
        st.error("Please enter both Question and AI Response.")
        st.stop()

    with st.spinner("🧠 AI Agents are evaluating the response..."):

        results = evaluate_response(
            question,
            ai_response,
            reference
        )

    relevance = results["relevance"]
    accuracy = results["accuracy"]
    hallucination = results["hallucination"]
    completeness = results["completeness"]
    overall = results["overall"]

    current_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        """
        <h2 style='text-align:center;'>
        📊 AI Evaluation Dashboard
        </h2>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("🎯 Relevance", f"{relevance:.2f}")
        st.progress(float(relevance))

    with c2:
        st.metric("✅ Accuracy", f"{accuracy:.2f}")
        st.progress(float(accuracy))

    with c3:
        st.metric("⚠ Hallucination", f"{hallucination:.2f}")
        st.progress(float(hallucination))

    with c4:
        st.metric("📄 Completeness", f"{completeness:.2f}")
        st.progress(float(completeness))

    st.markdown("---")

    left_chart, right_chart = st.columns([1.4, 1])

    with left_chart:

        fig = go.Figure()

        fig.add_trace(
            go.Scatterpolar(
                r=[
                    relevance,
                    accuracy,
                    hallucination,
                    completeness,
                    relevance
                ],
                theta=[
                    "Relevance",
                    "Accuracy",
                    "Hallucination",
                    "Completeness",
                    "Relevance"
                ],
                fill="toself",
                line=dict(width=3),
            )
        )

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )
            ),
            showlegend=False,
            template="plotly_dark",
            height=500,
            margin=dict(l=20, r=20, t=40, b=20)
        )

        st.plotly_chart(fig, use_container_width=True)

    with right_chart:

        st.subheader("🏆 Overall Quality")

        st.metric(
            "⭐ Final Score",
            f"{overall:.2f}",
            delta=f"{overall*100:.0f}%"
        )

        st.caption(f"🕒 Evaluation Time : {current_time}")

        st.progress(float(overall))

        st.markdown("")

        if overall >= 0.85:

            verdict = "Excellent"

            st.success(
                "🌟 Excellent Response\n\n"
                "Highly relevant, accurate and complete."
            )

        elif overall >= 0.70:

            verdict = "Good"

            st.info(
                "👍 Good Response\n\n"
                "Only minor improvements required."
            )

        elif overall >= 0.50:

            verdict = "Average"

            st.warning(
                "⚠ Average Response\n\n"
                "Needs better refinement."
            )

        else:

            verdict = "Poor"

            st.error(
                "❌ Poor Response\n\n"
                "Major improvements required."
            )

        st.markdown("---")

    history = pd.DataFrame([{
        "Time": current_time,
        "Question": question,
        "Overall Score": round(overall, 2),
        "Verdict": verdict
    }])

    if os.path.exists("evaluation_history.csv"):

        history.to_csv(
            "evaluation_history.csv",
            mode="a",
            header=False,
            index=False
        )

    else:

        history.to_csv(
            "evaluation_history.csv",
            index=False
        )

    st.subheader("📜 Evaluation History")

    history_df = pd.read_csv("evaluation_history.csv")

    st.dataframe(
        history_df,
        use_container_width=True
    )

    st.markdown("---")

    st.subheader("🤖 Agent Analysis")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            f"""
<div class="agent-card">
<b>🎯 Relevance Agent</b><br><br>
Score : <b>{relevance:.2f}</b>
</div>
""",
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
<div class="agent-card">
<b>✅ Accuracy Agent</b><br><br>
Score : <b>{accuracy:.2f}</b>
</div>
""",
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown(
            f"""
<div class="agent-card">
<b>⚠ Hallucination Agent</b><br><br>
Score : <b>{hallucination:.2f}</b>
</div>
""",
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
<div class="agent-card">
<b>📄 Completeness Agent</b><br><br>
Score : <b>{completeness:.2f}</b>
</div>
""",
            unsafe_allow_html=True,
        )

    st.markdown("---")

    st.subheader("📌 Performance Summary")

    summary = {
        "Relevance": relevance,
        "Accuracy": accuracy,
        "Hallucination": hallucination,
        "Completeness": completeness,
    }

    for metric, score in summary.items():

        if score >= 0.85:
            emoji = "🟢"

        elif score >= 0.70:
            emoji = "🟡"

        else:
            emoji = "🔴"

        st.write(f"{emoji} **{metric}** : {score:.2f}")




# ---------------- FOOTER ----------------


    

    st.subheader("📊 Score Comparison")

    chart_df = pd.DataFrame({
        "Metric": [
            "Relevance",
            "Accuracy",
            "Hallucination",
            "Completeness"
        ],
        "Score": [
            relevance,
            accuracy,
            hallucination,
            completeness
        ]
    })

    st.bar_chart(
        chart_df,
        x="Metric",
        y="Score",
        use_container_width=True
    )

    st.subheader("💡 AI Recommendations")

    recommendations = []

    if relevance < 0.80:
        recommendations.append(
            "🎯 Improve relevance by answering the user's question more directly."
        )

    if accuracy < 0.80:
        recommendations.append(
            "✅ Verify facts before generating the response."
        )

    if hallucination < 0.80:
        recommendations.append(
            "⚠ Reduce unsupported claims and avoid fabricated information."
        )

    if completeness < 0.80:
        recommendations.append(
            "📄 Cover more important points to improve completeness."
        )

    if len(recommendations) == 0:
        st.success("🎉 Excellent! No major improvements are required.")
    else:
        for rec in recommendations:
            st.info(rec)

    st.subheader("📋 Evaluation Summary")

    summary_df = pd.DataFrame({
        "Metric": [
            "Relevance",
            "Accuracy",
            "Hallucination",
            "Completeness",
            "Overall"
        ],
        "Score": [
            relevance,
            accuracy,
            hallucination,
            completeness,
            overall
        ]
    })

    st.dataframe(
        summary_df,
        use_container_width=True,
        hide_index=True
    )

    csv = summary_df.to_csv(index=False)

    st.download_button(
        label="📥 Download Evaluation Report (CSV)",
        data=csv,
        file_name="AI_Evaluation_Report.csv",
        mime="text/csv",
        use_container_width=True,
    )

    report = f"""
AI RESPONSE QUALITY REPORT

Evaluation Time :
{current_time}

Question
---------
{question}

AI Response
-----------
{ai_response}

Reference Answer
----------------
{reference}

Scores
------

Relevance : {relevance:.2f}

Accuracy : {accuracy:.2f}

Hallucination : {hallucination:.2f}

Completeness : {completeness:.2f}

Overall : {overall:.2f}

Verdict : {verdict}
"""

    
    st.download_button(
        label="📥 Download Evaluation Report (CSV)",
        data=csv,
        file_name="AI_Evaluation_Report.csv",
        mime="text/csv",
        use_container_width=True,
    )

    
