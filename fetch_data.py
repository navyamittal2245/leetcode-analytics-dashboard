import requests
import json
import streamlit as st

@st.cache_data(ttl=600)
def get_user_profile(username):
    url = "https://leetcode.com/graphql"
    query = """
    query userPublicProfile($username: String!) {
      matchedUser(username: $username) {
        username
        githubUrl
        twitterUrl
        linkedinUrl

        profile {
          realName
          userAvatar
          ranking
          reputation
          countryName
          school
          company
          jobTitle
          aboutMe
        }
      }
    }
    """
    payload = {
        "query": query,
        "variables": {
            "username": username
        }
    }
    response = requests.post(url, json=payload, timeout=10)
    response.raise_for_status()
    return response.json()

@st.cache_data(ttl=600)
def get_user_progress(username):
    url = "https://leetcode.com/graphql"
    query = """
    query userProfileUserQuestionProgressV2($userSlug: String!) {
      userProfileUserQuestionProgressV2(userSlug: $userSlug) {
        numAcceptedQuestions {
          difficulty
          count
        }
      }
    }
    """
    payload = {
        "query": query,
        "variables": {
            "userSlug": username
        }
    }
    response = requests.post(url, json=payload, timeout=10)
    response.raise_for_status()
    return response.json()

@st.cache_data(ttl=600)
def get_user_skills(username):
    url = "https://leetcode.com/graphql"
    query = """
    query skillStats($username: String!) {  
      matchedUser(username: $username) {
        tagProblemCounts {      
          advanced { 
            tagName 
            tagSlug 
            problemsSolved 
          }  
          intermediate { 
            tagName 
            tagSlug 
            problemsSolved 
          }      
          fundamental { 
            tagName 
            tagSlug 
            problemsSolved 
          } 
        } 
      }
    }
    """
    payload = {
        "query": query,
        "variables": {
            "username": username
        }
    }
    response = requests.post(url, json=payload, timeout=10)
    response.raise_for_status()
    return response.json()

@st.cache_data(ttl=600)
def get_user_contests(username):
    url = "https://leetcode.com/graphql"
    query = """
    query userContestRankingInfo($username: String!) {
      userContestRanking(username: $username) {
        attendedContestsCount
        rating
        globalRanking
        totalParticipants
        topPercentage
        badge {
          name
        }
      }

      userContestRankingHistory(username: $username) {
        attended
        trendDirection
        problemsSolved
        totalProblems
        finishTimeInSeconds
        rating
        ranking
        contest {
          title
          startTime
        }
      }
    }
    """
    payload = {
        "query": query,
        "variables": {
            "username": username
        }
    }
    response = requests.post(url, json=payload, timeout=10)
    response.raise_for_status()
    return response.json()

@st.cache_data(ttl=600)
def get_user_calendar(username):
    url = "https://leetcode.com/graphql"
    query = """
    query userProfileCalendar($username: String!) {  
      matchedUser(username: $username) {    
        userCalendar {
          activeYears      
          streak 
          totalActiveDays
          submissionCalendar
        }  
      }
    }
    """
    payload = {
        "query": query,
        "variables": {
            "username": username
        }
    }
    response = requests.post(url, json=payload, timeout=10)
    response.raise_for_status()
    return response.json()




