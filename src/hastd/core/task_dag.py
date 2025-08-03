from typing import List, Dict, Tuple
import networkx as nx


class TaskDAGBuilder:
    """
    Converts a list of structured field extraction tasks into a Directed Acyclic Graph (DAG),
    preserving hierarchical dependencies based on field paths.
    """

    def __init__(self, tasks: List[Dict]):
        """
        :param tasks: List of tasks returned by the schema parser. Each task must have a 'field_path'.
        """
        self.tasks = tasks
        self.graph = nx.DiGraph()

    def build(self) -> nx.DiGraph:
        """
        Constructs a DAG where each node is a field path, and edges represent parent-child nesting.
        """
        for task in self.tasks:
            field_path = task["field_path"]
            self.graph.add_node(field_path, task=task)

            # Identify parent based on nesting in the field path
            if "." in field_path:
                parent = ".".join(field_path.split(".")[:-1])
                if parent not in self.graph:
                    self.graph.add_node(parent)
                self.graph.add_edge(parent, field_path)
            elif "[]" in field_path:
                parent = field_path.replace("[]", "")
                if parent not in self.graph:
                    self.graph.add_node(parent)
                self.graph.add_edge(parent, field_path)

        return self.graph

    def get_execution_order(self) -> List[str]:
        """
        Returns an ordered list of task keys based on topological sort of the DAG.
        """
        return list(nx.topological_sort(self.graph))


# Optional CLI runner
if __name__ == "__main__":
    from pprint import pprint

    sample_tasks = [
        {"field_path": "author.name", "description": "Author name"},
        {"field_path": "author.email", "description": "Author email"},
        {"field_path": "title", "description": "Document title"},
        {"field_path": "references[].title", "description": "Reference title"},
    ]

    dag_builder = TaskDAGBuilder(sample_tasks)
    dag = dag_builder.build()

    print("🔁 Execution Order:")
    pprint(dag_builder.get_execution_order())

    print("\n📌 DAG Nodes:")
    pprint(dag.nodes(data=True))

    print("\n➡️ DAG Edges:")
    pprint(list(dag.edges()))
