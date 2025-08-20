import streamlit as st
import plotly.graph_objects as go
import random
import time

# --- 앱 초기 설정 ---

# 브라우저 탭에 표시될 제목과 아이콘 설정
st.set_page_config(page_title="간단 룰렛", page_icon="🎯")

# --- 세션 상태 초기화 ---
# Streamlit은 사용자가 위젯과 상호작용할 때마다 스크립트를 다시 실행합니다.
# 따라서, 앱의 상태(state)를 유지하려면 `st.session_state`를 사용해야 합니다.

# 'participants'가 세션 상태에 없으면, 빈 리스트로 초기화합니다.
if 'participants' not in st.session_state:
    st.session_state.participants = []

# 'winner'가 세션 상태에 없으면, None으로 초기화합니다.
if 'winner' not in st.session_state:
    st.session_state.winner = None

# --- 앱 UI 구성 ---

# 앱의 메인 제목
st.title("🎯 간단 룰렛")
st.write("---")

# 2개의 컬럼 생성 (입력창과 참여자 목록)
col1, col2 = st.columns([2, 1])

with col1:
    # 학생 이름 입력을 위한 텍스트 입력창
    names_input = st.text_input(
        "룰렛에 참여할 학생들의 이름을 쉼표(,)로 구분하여 입력하세요.",
        placeholder="예시) 홍길동, 이순신, 강감찬"
    )

    # "돌리기" 버튼
    if st.button("돌리기!", use_container_width=True):
        # 입력된 이름 문자열을 쉼표 기준으로 나누고, 공백을 제거하여 리스트로 만듭니다.
        participants = [name.strip() for name in names_input.split(',') if name.strip()]
        
        if len(participants) > 1:
            # 참여자가 2명 이상일 경우에만 룰렛을 실행합니다.
            st.session_state.participants = participants
            
            # 스피너(spinner)를 사용하여 룰렛이 돌아가는 듯한 효과를 줍니다.
            with st.spinner("룰렛을 돌리는 중입니다..."):
                time.sleep(2)  # 2초 동안 대기하여 긴장감을 줍니다.
            
            # 참여자 중에서 무작위로 한 명을 당첨자로 선택합니다.
            st.session_state.winner = random.choice(st.session_state.participants)
            
            # 당첨 축하 메시지와 함께 풍선 효과를 보여줍니다.
            st.balloons()
            st.success(f"🎉 축하합니다! **{st.session_state.winner}**님이 당첨되었습니다! 🎉")
        else:
            # 참여자가 1명 이하일 경우, 에러 메시지를 표시합니다.
            st.error("룰렛을 돌리려면 최소 2명 이상의 참여자가 필요합니다.")
            st.session_state.winner = None # 기존 당첨자 정보 초기화

with col2:
    # 현재 참여자 목록을 표시합니다.
    st.write("**참여자 목록**")
    if names_input:
        current_participants = [name.strip() for name in names_input.split(',') if name.strip()]
        st.write(current_participants)
    else:
        st.write("이름을 입력해주세요.")


# --- 결과 표시 ---

# 당첨자가 결정되면 룰렛 차트를 표시합니다.
if st.session_state.winner:
    participants = st.session_state.participants
    winner = st.session_state.winner
    
    # 각 참여자에게 동일한 크기의 파이 조각을 할당합니다.
    values = [10] * len(participants)
    
    # 당첨된 사람의 조각을 강조하기 위해 'pull' 값을 설정합니다.
    # 당첨자는 0.2만큼 조각이 튀어나오고, 나머지는 0입니다.
    pull_values = [0.2 if name == winner else 0 for name in participants]

    # Plotly를 사용하여 원형 차트(룰렛) 생성
    fig = go.Figure(data=[go.Pie(
        labels=participants, 
        values=values,
        pull=pull_values, # 당첨자 조각 강조
        hole=.3, # 중앙에 구멍을 뚫어 도넛 형태로 만듭니다.
        marker_colors=['#FFC300', '#FF5733', '#C70039', '#900C3F', '#581845'] # 색상 테마
    )])

    # 차트 레이아웃 설정
    fig.update_layout(
        title_text=f"✨ 오늘의 당첨자: {winner} ✨",
        title_x=0.5, # 제목을 중앙에 위치시킵니다.
        annotations=[dict(text='결과', x=0.5, y=0.5, font_size=20, showarrow=False)]
    )
    
    # Streamlit에 차트를 표시합니다.
    st.plotly_chart(fig, use_container_width=True)