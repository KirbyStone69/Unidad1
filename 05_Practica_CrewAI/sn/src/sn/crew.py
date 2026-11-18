from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import SerperDevTool 
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


filename = datetime.now().strftime("reports/report_%Y-%m-%d_%H-%M.md")

search_tool = SerperDevTool()

#cron

@CrewBase
class Sn():
    """Sn crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def researcher(self) -> Agent:
        return Agent(
        role="Investigador principal",
        goal="Investigar profundamente el tema solicitado y encontrar información confiable",
        backstory=(
            "Eres un investigador especializado en localizar, contrastar "
            "y sintetizar información proveniente de múltiples fuentes."
        ),
        tools=[search_tool],
        verbose=True,
        allow_delegation=False
    )


    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
        role="Analista y redactor",
        goal="Convertir la investigación recopilada en un reporte claro y estructurado",
        backstory=(
            "Eres un analista especializado en organizar información compleja "
            "y transformarla en reportes comprensibles y bien fundamentados."
        ),
        verbose=True,
        allow_delegation=False
    )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'], # type: ignore[index]
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['reporting_task'], # type: ignore[index]
            output_file=filename
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Sn crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )