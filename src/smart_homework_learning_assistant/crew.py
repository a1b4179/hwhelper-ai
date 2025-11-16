import os

from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import (
	SerplyWebSearchTool,
	ScrapeWebsiteTool,
	FileReadTool
)





@CrewBase
class SmartHomeworkLearningAssistantCrew:
    """SmartHomeworkLearningAssistant crew"""

    
    @agent
    def web_research_specialist(self) -> Agent:
        
        return Agent(
            config=self.agents_config["web_research_specialist"],
            
            
            tools=[				SerplyWebSearchTool(),
				ScrapeWebsiteTool()],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            max_execution_time=None,
            llm=LLM(
                model="openai/gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def educational_video_curator(self) -> Agent:
        
        return Agent(
            config=self.agents_config["educational_video_curator"],
            
            
            tools=[				SerplyWebSearchTool()],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            max_execution_time=None,
            llm=LLM(
                model="openai/gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def academic_solution_expert(self) -> Agent:
        
        return Agent(
            config=self.agents_config["academic_solution_expert"],
            
            
            tools=[				FileReadTool()],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            max_execution_time=None,
            llm=LLM(
                model="openai/gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    

    
    @task
    def research_topic_comprehensively(self) -> Task:
        return Task(
            config=self.tasks_config["research_topic_comprehensively"],
            markdown=False,
            
            
        )
    
    @task
    def find_educational_videos(self) -> Task:
        return Task(
            config=self.tasks_config["find_educational_videos"],
            markdown=False,
            
            
        )
    
    @task
    def create_complete_educational_solution(self) -> Task:
        return Task(
            config=self.tasks_config["create_complete_educational_solution"],
            markdown=False,
            
            
        )
    

    @crew
    def crew(self) -> Crew:
        """Creates the SmartHomeworkLearningAssistant crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )

    def _load_response_format(self, name):
        with open(os.path.join(self.base_directory, "config", f"{name}.json")) as f:
            json_schema = json.loads(f.read())

        return SchemaConverter.build(json_schema)
