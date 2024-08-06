import streamlit as st, pandas as pd, plotly.express as px

st.set_page_config(
    page_title="Call Center Dashboard ☎️",
    page_icon="☎️",
    layout='wide'
)

@st.cache_data
def GetExcelData():
    df = pd.read_excel(r"C:\Users\roylo\OneDrive\Documentos\Data Science\Proyectos\Call Center\src\Datasets\callCenter.xlsx", engine='openpyxl')
    return df

callCenter = GetExcelData()

with st.sidebar:
    st.markdown("# Call Center")
    st.image('Images/callCenterLogo.png')

    st.title("Filter Here: ")

    agentFilter = st.multiselect(
        label='Agent',
        options=callCenter['Agent'].unique(),
        default=callCenter['Agent'].unique()
    )

    departmentFilter = st.multiselect(
        label='Department',
        options=callCenter['Department'].unique(),
        default=callCenter['Department'].unique()
    )

    answeredFilter = st.multiselect(
        label="Answered",
        options=callCenter['Answered'].unique(),
        default=callCenter['Answered'].unique()
    )

    resolvedFilter = st.multiselect(
        label='Resolved',
        options=callCenter['Resolved'].unique(),
        default=callCenter['Resolved'].unique()
    )

    minRatingFilter, maxRatingFilter = st.select_slider(
        label='Rating',
        options=sorted(callCenter['SatisfactionRating'].unique()),
        value=[callCenter['SatisfactionRating'].min(), callCenter['SatisfactionRating'].max()]
    )

    minDate, maxDate = st.select_slider(
        label='Date',
        options=callCenter['Date'].unique(),
        value=[callCenter['Date'].min(), callCenter['Date'].max()]
    )

callCenterFiltered = callCenter.query(
    "Agent == @agentFilter & Department == @departmentFilter & Answered == @answeredFilter & Resolved == @resolvedFilter & (SatisfactionRating >= @minRatingFilter & SatisfactionRating <= @maxRatingFilter) & (Date >= @minDate & Date <= @maxDate)"
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    totalCalls = callCenterFiltered.shape[0]
    st.markdown(f"## Total Calls 📞 : {totalCalls}")

with col2:
    avgRating = callCenterFiltered['SatisfactionRating'].mean()
    st.markdown(f"## Average Satisfaction Rating : {avgRating:,.2f} {"⭐" * round(avgRating)}")

with col3:
    avgRespondTime = callCenterFiltered['SpeedOfAnswer'].mean()
    st.markdown(f"## Average Speed of Response ⌛ : {avgRespondTime:,.2f} seconds")

with col4:
    avgTalkDuration = callCenterFiltered['AvgTalkDuration(Seconds)'].mean()
    st.markdown(f"## Average Talk Duration ⏱️ : {avgTalkDuration:,.2f} seconds.")

st.markdown("---")

col5, col6 = st.columns(2)

with col5:
    tab1, tab2 = st.tabs(['Date', 'Hour'])

    with tab1:
        callsCountByDate = callCenterFiltered.groupby('Date')['Date'].count()
        fig_callsCountByDate = px.line(
            title="Total Calls by Date",
            data_frame=callsCountByDate
        )
        fig_callsCountByDate.update_layout(
            title={
                'text' : "Total Calls by Date",
                'font' : {'size':30}
            },
            yaxis_title='Total Calls',
            xaxis_title='Date'
        )
        st.plotly_chart(fig_callsCountByDate)
    
    with tab2:
        callsCountByHour = callCenterFiltered.groupby('Hour')['Hour'].count()
        fig_callCountByHour = px.line(
            data_frame=callsCountByHour,
            title="Total Calls by Hour"
        )
        fig_callCountByHour.update_layout(
            title={
                'text':'Total Calls by Hour',
                'font':{'size':30}
            },
            xaxis_title='Hour'

        )
        st.plotly_chart(fig_callCountByHour)

with col6:
    tab3, tab4 = st.tabs(['Agents And Departments', 'Speed of Answer and Talk Duration'])

    with tab3:
        callsCountByAgentsDepartments = callCenterFiltered.groupby(by=['Agent', "Department"])['CallId'].count().reset_index()

        fig_callCountByAgentDepartments = px.bar(
            data_frame=callsCountByAgentsDepartments,
            x='CallId',
            y='Agent',
            color='Department',
            text='Department',
            orientation='h',
            title="Total Calls by Agent and Department",
            width=1000
        )
        fig_callCountByAgentDepartments.update_layout(
            title= {'text' : 'Total Calls by Agent and Department',
            'font' : {'size':30}
            },
            xaxis_title='Total Calls'
        )
        st.plotly_chart(fig_callCountByAgentDepartments)

    with tab4:
        fig_callsCountBySpeedOfAnswerTalkDuration = px.scatter(
            data_frame=callCenterFiltered,
            x='SpeedOfAnswer',
            y='AvgTalkDuration(Seconds)',
            color='Resolved'
        )
        st.plotly_chart(fig_callsCountBySpeedOfAnswerTalkDuration)