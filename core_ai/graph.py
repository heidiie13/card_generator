from core_ai.utils.nodes import (
    llm_node,
    dominant_color_node,
    merge_node,
    add_text_node,
    route_random_template,
    random_template_node,
    font_color_node, 
)

from core_ai.utils.state import State
from langgraph.graph import StateGraph

def build_birthday_card_graph() -> StateGraph:
    graph_builder = StateGraph(State)

    graph_builder.add_node("input", lambda state: state)
    graph_builder.add_node("dominant_color", dominant_color_node)
    graph_builder.add_node("llm", llm_node)
    graph_builder.add_node("random_template", random_template_node)
    graph_builder.add_node("font_color", font_color_node)
    graph_builder.add_node("merge", merge_node)
    graph_builder.add_node("add_text", add_text_node)

    graph_builder.add_edge("input", "llm")
    graph_builder.add_conditional_edges("llm", route_random_template, {"dominant_color":"dominant_color", "random_template":"random_template"})
    graph_builder.add_edge("random_template", "dominant_color")
    graph_builder.add_edge("dominant_color", "font_color")
    graph_builder.add_edge("font_color", "merge")
    graph_builder.add_edge("merge", "add_text")
    graph_builder.add_edge("add_text", "__end__")

    graph_builder.set_entry_point("input")

    graph = graph_builder.compile()
    return graph