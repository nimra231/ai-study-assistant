"""Study Planner - Create study schedules."""
from datetime import datetime, timedelta
from typing import List, Dict
import streamlit as st
from modules.embeddings_manager import get_embeddings_manager


class StudyPlanner:
    def __init__(self):
        self.embeddings_manager = get_embeddings_manager()

    def _get_topics(self):
        if self.embeddings_manager.vector_store is None:
            return []
        return self.embeddings_manager.get_document_names()

    def create_study_plan(self, exam_date, daily_hours, topics=None, study_style="balanced", break_interval=45):
        today = datetime.now()
        days_until_exam = (exam_date - today).days

        if days_until_exam < 1:
            return {"error": "Exam date must be in the future!", "plan": []}

        if not topics:
            topics = self._get_topics()

        if not topics:
            return {"error": "No study materials uploaded.", "plan": []}

        total_hours = days_until_exam * daily_hours
        plan = []
        current_date = today

        for day in range(days_until_exam):
            current_date = today + timedelta(days=day)
            topic_index = day % len(topics)
            primary_topic = topics[topic_index]

            daily_plan = {
                "date": current_date.strftime("%Y-%m-%d (%A)"),
                "day_number": day + 1,
                "total_hours": daily_hours,
                "primary_topic": primary_topic,
                "sessions": self._create_sessions(daily_hours, break_interval, primary_topic),
                "goals": [f"Understand {primary_topic}", "Review key concepts", "Practice problems"],
            }
            plan.append(daily_plan)

        return {
            "exam_date": exam_date.strftime("%Y-%m-%d"),
            "days_until_exam": days_until_exam,
            "total_study_hours": total_hours,
            "topics": topics,
            "daily_hours": daily_hours,
            "study_style": study_style,
            "plan": plan,
        }

    def _create_sessions(self, daily_hours, break_interval, topic):
        sessions = []
        remaining = daily_hours
        session_num = 1
        while remaining > 0:
            duration = min(2, remaining)
            sessions.append({
                "session": session_num,
                "duration": f"{duration}h",
                "topic": topic,
                "activity": "Focus study" if session_num == 1 else "Practice & review",
                "break_after": f"{break_interval} min" if remaining > duration else "Done!",
            })
            remaining -= duration
            session_num += 1
        return sessions


_study_planner = None

def get_study_planner():
    global _study_planner
    if _study_planner is None:
        _study_planner = StudyPlanner()
    return _study_planner
