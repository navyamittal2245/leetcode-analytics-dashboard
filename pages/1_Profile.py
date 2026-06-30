import streamlit as st

profile = st.session_state.get("profile")

if profile is None:
    st.warning(" Please enter a username on the Home page first.")
    st.stop()

user = profile["data"]["matchedUser"]
profile_info = user["profile"]

st.title("👤 User Profile")

profile_col1, profile_col2 = st.columns([1, 2.5])

with profile_col1:
    # Handle user avatar
    avatar_url = profile_info.get("userAvatar") or "https://assets.leetcode.com/users/default_avatar.jpg"
    st.image(avatar_url, width=150)
    
    # Handle about me
    about = profile_info.get("aboutMe")
    if about and about.strip():
        st.markdown(f"*{about.strip()}*")
    else:
        st.markdown("*No bio available.*")

with profile_col2:
    username = user.get("username", "Unknown")
    st.subheader(username)

    name = profile_info.get("realName") or "Not provided"
    country = profile_info.get("countryName") or "Not provided"
    school = profile_info.get("school") or "Not provided"
    company = profile_info.get("company") or "Not provided"
    job = profile_info.get("jobTitle") or "Not provided"

    st.markdown(f"** Real Name:** {name}")
    st.markdown(f"** Location:** {country}")
    st.markdown(f"** Education:** {school}")
    
    if company != "Not provided" or job != "Not provided":
        company_job = f"{company} ({job})" if (company != "Not provided" and job != "Not provided") else (company if company != "Not provided" else job)
        st.markdown(f"** Profession:** {company_job}")
    else:
        st.markdown("** Profession:** Not provided")

st.divider()

# Profile Key Metrics
col1, col2 = st.columns(2)
with col1:
    ranking = profile_info.get("ranking")
    ranking_str = f"{ranking:,}" if ranking is not None else "N/A"
    st.metric("🏆 Global LeetCode Rank", ranking_str)
with col2:
    reputation = profile_info.get("reputation")
    rep_str = f"{reputation:,}" if reputation is not None else "0"
    st.metric("⭐ Reputation Points", rep_str)

st.divider()

st.subheader("🔗 Social Links")
github = user.get("githubUrl")
linkedin = user.get("linkedinUrl")
twitter = user.get("twitterUrl")

social_cols = st.columns(3)
has_socials = False

if github:
    has_socials = True
    with social_cols[0]:
        st.link_button(" GitHub Profile", github, use_container_width=True)

if linkedin:
    has_socials = True
    with social_cols[1]:
        st.link_button(" LinkedIn Profile", linkedin, use_container_width=True)

if twitter:
    has_socials = True
    with social_cols[2]:
        st.link_button(" Twitter Profile", twitter, use_container_width=True)

if not has_socials:
    st.info("No external social links are linked to this LeetCode profile.")
