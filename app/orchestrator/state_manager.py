from __future__ import annotations

from app.models.schemas import StepDefinition, StepResult, StepStatus, TaskRecord


class StateManager:
    @staticmethod
    def dependency_outputs(task: TaskRecord, step: StepDefinition) -> dict[int, dict]:
        outputs: dict[int, dict] = {}
        for dependency_id in step.depends_on:
            result = task.results.get(dependency_id)
            if result and result.status == StepStatus.completed:
                outputs[dependency_id] = result.output
        return outputs

    @staticmethod
    def ready_steps(task: TaskRecord) -> list[StepDefinition]:
        ready: list[StepDefinition] = []
        completed = {
            step_id for step_id, result in task.results.items() if result.status == StepStatus.completed
        }
        active = {
            step_id
            for step_id, result in task.results.items()
            if result.status in {StepStatus.queued, StepStatus.running}
        }

        for step in task.steps:
            if step.step_id in completed or step.step_id in active:
                continue
            if all(dep in completed for dep in step.depends_on):
                ready.append(step)
        return ready

    @staticmethod
    def all_steps_completed(task: TaskRecord) -> bool:
        return bool(task.steps) and all(
            task.results.get(step.step_id) and task.results[step.step_id].status == StepStatus.completed
            for step in task.steps
        )

    @staticmethod
    def any_step_failed(task: TaskRecord) -> bool:
        return any(result.status == StepStatus.failed for result in task.results.values())
