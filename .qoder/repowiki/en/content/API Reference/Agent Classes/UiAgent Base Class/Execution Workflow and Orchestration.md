# Execution Workflow and Orchestration

<cite>
**Referenced Files in This Document**
- [agent.py](file://src/page_eyes/agent.py)
- [deps.py](file://src/page_eyes/deps.py)
- [prompt.py](file://src/page_eyes/prompt.py)
- [_base.py](file://src/page_eyes/tools/_base.py)
- [device.py](file://src/page_eyes/device.py)
- [config.py](file://src/page_eyes/config.py)
- [report_template.html](file://src/page_eyes/report_template.html)
- [test_web_agent.py](file://tests/test_web_agent.py)
- [test_planning_agent.py](file://tests/test_planning_agent.py)
</cite>

## Table of Contents
1. [Introduction](#introduction)
2. [Project Structure](#project-structure)
3. [Core Components](#core-components)
4. [Architecture Overview](#architecture-overview)
5. [Detailed Component Analysis](#detailed-component-analysis)
6. [Dependency Analysis](#dependency-analysis)
7. [Performance Considerations](#performance-considerations)
8. [Troubleshooting Guide](#troubleshooting-guide)
9. [Conclusion](#conclusion)
10. [Appendices](#appendices)

## Introduction
This document explains the execution workflow and orchestration capabilities of the UiAgent base class. It covers the run() method’s end-to-end flow, including planning agent integration, step-by-step execution, error handling via mark_failed(), usage tracking, and reporting. It also details the _sub_agent_run() helper, context management through RunContext, and step-by-step logging via handle_graph_node(). Practical examples, error recovery strategies, parallel tool execution constraints, step validation, and termination conditions are included for robust operation.

## Project Structure
The UiAgent orchestrates planning, execution, tool invocation, and reporting across platforms (web, Android, iOS, Harmony, Electron). The core runtime resides in the agent module, with orchestration logic in UiAgent, planning logic in PlanningAgent, tooling in AgentTool, and shared context/state in deps.

```mermaid
graph TB
subgraph "Agent Runtime"
UA["UiAgent<br/>run(), _sub_agent_run(), handle_graph_node()"]
PA["PlanningAgent<br/>run()"]
AG["Agent[pydantic_ai]<br/>configured with tools/capabilities"]
end
subgraph "Context & State"
AC["AgentContext<br/>steps, current_step"]
SI["StepInfo<br/>step, description, action, params,<br/>image_url, screen_elements, is_success"]
DP["AgentDeps<br/>settings, device, tool, context"]
end
subgraph "Tools & Devices"
AT["AgentTool<br/>tool decorators, get_screen, mark_failed, tear_down"]
DEV["Device<br/>Web/Android/iOS/Harmony/Electron"]
end
subgraph "Prompts & Config"
PR["SYSTEM_PROMPT / PLANNING_SYSTEM_PROMPT"]
CFG["Settings / default_settings"]
end
UA --> PA
UA --> AG
UA --> DP
DP --> AC
DP --> AT
DP --> DEV
AG --> AT
UA --> PR
UA --> CFG
```

**Diagram sources**
- [agent.py:96-314](file://src/page_eyes/agent.py#L96-L314)
- [deps.py:48-82](file://src/page_eyes/deps.py#L48-L82)
- [_base.py:130-391](file://src/page_eyes/tools/_base.py#L130-L391)
- [device.py:42-390](file://src/page_eyes/device.py#L42-L390)
- [prompt.py:8-166](file://src/page_eyes/prompt.py#L8-L166)
- [config.py:54-73](file://src/page_eyes/config.py#L54-L73)

**Section sources**
- [agent.py:96-314](file://src/page_eyes/agent.py#L96-L314)
- [deps.py:48-82](file://src/page_eyes/deps.py#L48-L82)
- [prompt.py:8-166](file://src/page_eyes/prompt.py#L8-L166)
- [config.py:54-73](file://src/page_eyes/config.py#L54-L73)

## Core Components
- UiAgent: Orchestrates planning, step iteration, tool execution, error handling, and reporting. Provides run(), _sub_agent_run(), handle_graph_node().
- PlanningAgent: Decomposes user intent into atomic PlanningStep sequences using a dedicated system prompt.
- AgentTool: Defines tool wrappers and utilities (get_screen, mark_failed, tear_down) with pre/post handlers and decorators.
- AgentDeps: Holds Settings, Device, Tool, and AgentContext for cross-module coordination.
- AgentContext/StepInfo: Tracks per-step metadata, success/failure, and screen state.
- RunContext: Provides runtime context for tool execution and usage tracking.

**Section sources**
- [agent.py:96-314](file://src/page_eyes/agent.py#L96-L314)
- [agent.py:73-90](file://src/page_eyes/agent.py#L73-L90)
- [_base.py:130-391](file://src/page_eyes/tools/_base.py#L130-L391)
- [deps.py:48-82](file://src/page_eyes/deps.py#L48-L82)
- [deps.py:35-73](file://src/page_eyes/deps.py#L35-L73)

## Architecture Overview
The UiAgent integrates a planning phase with a strict execution loop. PlanningAgent produces a sequence of PlanningStep items. UiAgent iterates each step, invoking a sub-agent run for each step, enforcing single-tool-at-a-time constraints, capturing screenshots, and aggregating usage metrics. Failures are recorded via mark_failed() and terminate the current step; the overall run stops if any step fails unless explicitly handled.

```mermaid
sequenceDiagram
participant User as "Caller"
participant UA as "UiAgent"
participant PA as "PlanningAgent"
participant AG as "Agent[pydantic_ai]"
participant CTX as "RunContext"
participant TOOL as "AgentTool"
participant REP as "Report"
User->>UA : run(prompt, system_prompt?, report_dir?)
UA->>PA : run(prompt)
PA-->>UA : AgentRunResult[PlanningOutputType]
UA->>CTX : create RunContext(deps, model, usage=Usage)
loop For each PlanningStep
UA->>UA : add_step_info(StepInfo(step, planning, description))
alt instruction != "结束任务"
UA->>AG : agent.iter(user_prompt=instruction, deps=deps, usage=usage)
AG-->>UA : iter nodes (UserPrompt, ModelRequest, CallTools)
UA->>UA : handle_graph_node(node) for logging
AG-->>UA : result (output, usage)
UA->>UA : update usage = result.usage()
UA->>TOOL : get_screen(parse_element=False) if missing image
else instruction == "结束任务"
UA->>TOOL : tear_down(action="tear_down", instruction="任务完成")
end
UA->>UA : check current_step.is_success
alt not success
UA->>TOOL : mark_failed(reason) via deps.tool.mark_failed
UA-->>User : break execution
end
end
UA->>REP : create_report(json_data, report_dir)
UA-->>User : return {is_success, steps, report_path}
```

**Diagram sources**
- [agent.py:225-314](file://src/page_eyes/agent.py#L225-L314)
- [agent.py:217-224](file://src/page_eyes/agent.py#L217-L224)
- [agent.py:192-216](file://src/page_eyes/agent.py#L192-L216)
- [agent.py:73-90](file://src/page_eyes/agent.py#L73-L90)
- [_base.py:322-346](file://src/page_eyes/tools/_base.py#L322-L346)

**Section sources**
- [agent.py:225-314](file://src/page_eyes/agent.py#L225-L314)
- [agent.py:217-224](file://src/page_eyes/agent.py#L217-L224)
- [agent.py:192-216](file://src/page_eyes/agent.py#L192-L216)

## Detailed Component Analysis

### UiAgent.run(): End-to-End Execution Flow
- Planning: Invokes PlanningAgent.run(prompt) to produce a PlanningOutputType containing steps.
- Step Iteration: Adds a sentinel “结束任务” step to finalize teardown.
- Per-Step Execution:
  - Creates RunContext with deps, model, and empty Usage.
  - Logs step header and description.
  - If instruction is not the sentinel:
    - Calls _sub_agent_run(planning, usage) to execute the step.
    - On success, updates usage and logs the output.
    - On UnexpectedModelBehavior, marks failure via deps.tool.mark_failed and logs the error.
  - After each step, ensures a screenshot exists (get_screen with parse_element=False) if none captured.
  - Checks current_step.is_success; if false, breaks the loop.
- Finalization:
  - Builds a report JSON with is_success, device_size, and steps.
  - Generates HTML report via create_report() and returns structured results.

```mermaid
flowchart TD
Start([Start run]) --> Plan["PlanningAgent.run(prompt)"]
Plan --> Steps["steps + sentinel '结束任务'"]
Steps --> Loop{"For each step"}
Loop --> |instruction != '结束任务'| Exec["_sub_agent_run(step, usage)"]
Exec --> UpdateUsage["usage = result.usage()"]
UpdateUsage --> LogOut["log output"]
LogOut --> Screenshot["get_screen(parse_element=False) if missing"]
Screenshot --> CheckSuccess{"current_step.is_success?"}
CheckSuccess --> |No| MarkFail["mark_failed(reason)"]
MarkFail --> Break([Break])
CheckSuccess --> |Yes| NextStep["Next step"]
Loop --> |instruction == '结束任务'| TearDown["tear_down(action='tear_down')"]
TearDown --> Screenshot2["get_screen(parse_element=False) if missing"]
Screenshot2 --> NextStep
NextStep --> Loop
Break --> BuildReport["create_report(json_data)"]
Loop --> |Done| BuildReport
BuildReport --> Return([Return {is_success, steps, report_path}])
```

**Diagram sources**
- [agent.py:225-314](file://src/page_eyes/agent.py#L225-L314)
- [_base.py:322-346](file://src/page_eyes/tools/_base.py#L322-L346)

**Section sources**
- [agent.py:225-314](file://src/page_eyes/agent.py#L225-L314)

### PlanningAgent Integration and Step Decomposition
- PlanningAgent constructs an Agent with PLANNING_SYSTEM_PROMPT and output type PlanningOutputType.
- It runs the user prompt and returns an AgentRunResult containing steps.
- The UiAgent appends a sentinel PlanningStep with instruction "结束任务" to trigger teardown.

```mermaid
sequenceDiagram
participant UA as "UiAgent"
participant PA as "PlanningAgent"
participant PAgent as "Agent(PLANNING_SYSTEM_PROMPT)"
UA->>PA : run(prompt)
PA->>PAgent : agent.run(prompt)
PAgent-->>PA : AgentRunResult[PlanningOutputType]
PA-->>UA : result
```

**Diagram sources**
- [agent.py:73-90](file://src/page_eyes/agent.py#L73-L90)
- [prompt.py:8-28](file://src/page_eyes/prompt.py#L8-L28)

**Section sources**
- [agent.py:73-90](file://src/page_eyes/agent.py#L73-L90)
- [prompt.py:8-28](file://src/page_eyes/prompt.py#L8-L28)

### _sub_agent_run(): Sub-Agent Execution Helper
- Wraps agent.iter(...) with async iteration over nodes.
- For each node, delegates to handle_graph_node() for logging.
- Returns the final AgentRunResult for usage accumulation.

```mermaid
sequenceDiagram
participant UA as "UiAgent"
participant AG as "Agent"
UA->>AG : agent.iter(user_prompt, deps, usage)
loop For each node
AG-->>UA : node
UA->>UA : handle_graph_node(node)
end
AG-->>UA : result
UA-->>UA : return result
```

**Diagram sources**
- [agent.py:217-224](file://src/page_eyes/agent.py#L217-L224)
- [agent.py:192-216](file://src/page_eyes/agent.py#L192-L216)

**Section sources**
- [agent.py:217-224](file://src/page_eyes/agent.py#L217-L224)
- [agent.py:192-216](file://src/page_eyes/agent.py#L192-L216)

### handle_graph_node(): Step-by-Step Logging
- Logs user prompts, tool results, and tool calls.
- Detects parallel tool calls by counting ToolCallPart entries and sets current_step.parallel_tool_calls accordingly.

```mermaid
flowchart TD
Enter([handle_graph_node]) --> Type{"Node type?"}
Type --> |UserPromptNode| LogUser["Log user task"]
Type --> |ModelRequestNode| LogToolRes["Log tool result"]
Type --> |CallToolsNode| Detect["Count ToolCallPart<br/>set parallel_tool_calls"]
LogUser --> Exit([Exit])
LogToolRes --> Exit
Detect --> Exit
```

**Diagram sources**
- [agent.py:192-216](file://src/page_eyes/agent.py#L192-L216)

**Section sources**
- [agent.py:192-216](file://src/page_eyes/agent.py#L192-L216)

### Context Management via RunContext and AgentContext
- RunContext is created with deps, model, and an empty Usage accumulator.
- AgentContext maintains an ordered mapping of steps and the current step pointer.
- ToolHandler enforces single-tool-at-a-time by checking current_step.parallel_tool_calls and raising ModelRetry if violated.

```mermaid
classDiagram
class RunContext {
+deps
+model
+usage
+prompt
}
class AgentContext {
+steps : OrderedDict[int, StepInfo]
+current_step : StepInfo
+add_step_info(step_info)
+update_step_info(**kwargs)
+set_step_failed(reason)
}
class StepInfo {
+step : int
+description : str
+action : str
+params : dict
+image_url : str
+screen_elements : list
+parallel_tool_calls : bool
+is_success : bool
}
RunContext --> AgentContext : "holds"
AgentContext --> StepInfo : "manages"
```

**Diagram sources**
- [agent.py:246-249](file://src/page_eyes/agent.py#L246-L249)
- [deps.py:48-82](file://src/page_eyes/deps.py#L48-L82)
- [deps.py:35-73](file://src/page_eyes/deps.py#L35-L73)
- [_base.py:39-86](file://src/page_eyes/tools/_base.py#L39-L86)

**Section sources**
- [agent.py:246-249](file://src/page_eyes/agent.py#L246-L249)
- [deps.py:48-82](file://src/page_eyes/deps.py#L48-L82)
- [deps.py:35-73](file://src/page_eyes/deps.py#L35-L73)
- [_base.py:39-86](file://src/page_eyes/tools/_base.py#L39-L86)

### Tool Execution, Parallel Constraints, and Atomic Actions
- Tools are decorated with @tool and registered via AgentTool.tools.
- ToolHandler pre_handle() records params/action and enforces single-tool-at-a-time by raising ModelRetry when parallel_tool_calls is true.
- Tools like get_screen capture images and optionally parse elements; mark_failed records failure and halts the current step.

```mermaid
flowchart TD
PreHandle["ToolHandler.pre_handle()"] --> CheckParallel{"parallel_tool_calls?"}
CheckParallel --> |Yes| Retry["raise ModelRetry('only use one tool at a time')"]
CheckParallel --> |No| Record["record params/action in current_step"]
Record --> Execute["execute tool"]
Execute --> PostHandle["ToolHandler.post_handle(result)"]
PostHandle --> Done([Done])
```

**Diagram sources**
- [_base.py:39-86](file://src/page_eyes/tools/_base.py#L39-L86)
- [_base.py:130-151](file://src/page_eyes/tools/_base.py#L130-L151)
- [_base.py:322-346](file://src/page_eyes/tools/_base.py#L322-L346)

**Section sources**
- [_base.py:39-86](file://src/page_eyes/tools/_base.py#L39-L86)
- [_base.py:130-151](file://src/page_eyes/tools/_base.py#L130-L151)
- [_base.py:322-346](file://src/page_eyes/tools/_base.py#L322-L346)

### Error Handling with mark_failed() and Termination Conditions
- On UnexpectedModelBehavior during step execution, UiAgent calls deps.tool.mark_failed() and logs the error.
- After each step, if current_step.is_success is False, the loop breaks, terminating further execution.
- tear_down() is invoked upon encountering the sentinel “结束任务” step.

```mermaid
flowchart TD
TryExec["Try _sub_agent_run(step, usage)"] --> Success{"UnexpectedModelBehavior?"}
Success --> |No| Continue([Continue])
Success --> |Yes| Mark["mark_failed(reason)"]
Mark --> LogErr["log error"]
LogErr --> Break([Break])
Continue --> CheckStep{"current_step.is_success?"}
CheckStep --> |No| Break
CheckStep --> |Yes| Next([Next step])
```

**Diagram sources**
- [agent.py:259-271](file://src/page_eyes/agent.py#L259-L271)
- [_base.py:322-346](file://src/page_eyes/tools/_base.py#L322-L346)

**Section sources**
- [agent.py:259-271](file://src/page_eyes/agent.py#L259-L271)
- [_base.py:322-346](file://src/page_eyes/tools/_base.py#L322-L346)

### Usage Tracking and Reporting
- Usage accumulates across steps via result.usage() after each successful step.
- A report JSON is built with is_success, device_size, and steps, then rendered to an HTML report via create_report().

```mermaid
sequenceDiagram
participant UA as "UiAgent"
participant REP as "create_report()"
UA->>UA : usage = result.usage()
UA->>REP : create_report(json_data, report_dir)
REP-->>UA : report_path
```

**Diagram sources**
- [agent.py:246-263](file://src/page_eyes/agent.py#L246-L263)
- [agent.py:171-191](file://src/page_eyes/agent.py#L171-L191)
- [report_template.html:1-45](file://src/page_eyes/report_template.html#L1-L45)

**Section sources**
- [agent.py:246-263](file://src/page_eyes/agent.py#L246-L263)
- [agent.py:171-191](file://src/page_eyes/agent.py#L171-L191)
- [report_template.html:1-45](file://src/page_eyes/report_template.html#L1-L45)

## Dependency Analysis
UiAgent depends on:
- PlanningAgent for decomposition into PlanningStep sequences.
- AgentTool for atomic actions and state capture.
- AgentContext/StepInfo for per-step state and success tracking.
- RunContext for usage and runtime context.
- Settings for model configuration and environment overrides.

```mermaid
graph LR
UA["UiAgent"] --> PA["PlanningAgent"]
UA --> AG["Agent[pydantic_ai]"]
UA --> DP["AgentDeps"]
DP --> AC["AgentContext"]
DP --> AT["AgentTool"]
DP --> DEV["Device"]
AG --> AT
UA --> CFG["Settings"]
```

**Diagram sources**
- [agent.py:96-314](file://src/page_eyes/agent.py#L96-L314)
- [deps.py:48-82](file://src/page_eyes/deps.py#L48-L82)
- [config.py:54-73](file://src/page_eyes/config.py#L54-L73)

**Section sources**
- [agent.py:96-314](file://src/page_eyes/agent.py#L96-L314)
- [deps.py:48-82](file://src/page_eyes/deps.py#L48-L82)
- [config.py:54-73](file://src/page_eyes/config.py#L54-L73)

## Performance Considerations
- Single-tool-at-a-time enforcement prevents race conditions and reduces ambiguity in state transitions.
- get_screen() is called after steps to ensure visual grounding; avoid redundant captures by checking current_step.image_url.
- Usage accumulation per step enables cost-awareness and budgeting across long executions.
- Parallel tool detection helps catch misconfigured plans early.

[No sources needed since this section provides general guidance]

## Troubleshooting Guide
Common issues and remedies:
- UnexpectedModelBehavior during step execution:
  - Symptom: Exception raised mid-step.
  - Action: UiAgent catches it, calls mark_failed(), logs the error, and terminates the current step.
- Tool concurrency violations:
  - Symptom: ModelRetry indicating only one tool at a time.
  - Action: Ensure the plan decomposes into atomic actions; do not request multiple concurrent tool calls.
- Missing screenshots after actions:
  - Symptom: Lack of visual context for subsequent steps.
  - Action: UiAgent automatically calls get_screen(parse_element=False) if image_url is empty after a step.
- Teardown failures:
  - Symptom: Sentinel step not reached or teardown not executed.
  - Action: Ensure the planning ends with instruction "结束任务".

**Section sources**
- [agent.py:259-271](file://src/page_eyes/agent.py#L259-L271)
- [_base.py:39-86](file://src/page_eyes/tools/_base.py#L39-L86)
- [agent.py:277-284](file://src/page_eyes/agent.py#L277-L284)

## Conclusion
UiAgent provides a robust, stepwise orchestration framework integrating planning, execution, tooling, and reporting. Its emphasis on atomic actions, single-tool-at-a-time execution, and explicit failure signaling yields reliable automation across diverse devices and modalities. The RunContext and AgentContext abstractions enable precise usage tracking and step-level diagnostics, while the report generation supports post-execution review and auditing.

[No sources needed since this section summarizes without analyzing specific files]

## Appendices

### Example Execution Patterns
- Web automation with multiple steps and assertions:
  - See [test_web_agent.py:11-22](file://tests/test_web_agent.py#L11-L22) for a composite interaction including navigation, scrolling, clicking, and waiting.
- Planning decomposition verification:
  - See [test_planning_agent.py:12-27](file://tests/test_planning_agent.py#L12-L27) for validating PlanningOutputType steps.

**Section sources**
- [test_web_agent.py:11-22](file://tests/test_web_agent.py#L11-L22)
- [test_planning_agent.py:12-27](file://tests/test_planning_agent.py#L12-L27)