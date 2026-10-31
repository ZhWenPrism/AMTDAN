import unittest

from amtdan.datasets import TaskRegistry, TaskSpec


class RegistrySnapshotTests(unittest.TestCase):
    def test_task_labels_do_not_follow_caller_mutation(self):
        labels = ["none", "mild", "moderate", "marked", "severe"]
        task = TaskSpec("task", labels)
        labels[0] = "changed"
        labels.pop()
        self.assertEqual(task.severity_labels, ("none", "mild", "moderate", "marked", "severe"))

    def test_registry_keeps_its_validated_tasks(self):
        labels = ("none", "mild", "moderate", "marked", "severe")
        tasks = [TaskSpec(f"task-{i}", labels) for i in range(17)]
        registry = TaskRegistry(tasks)
        tasks.clear()
        self.assertEqual(len(registry.tasks), 17)
        self.assertEqual(registry.by_name("task-16").name, "task-16")
