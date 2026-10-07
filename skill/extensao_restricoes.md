
---

# EXTENSION: Organizational Constraints

Apply this extension whenever the user provides organizational constraints: rules, policies, guidelines,
standards or legal and regulatory obligations that the organization requires every solution to follow.
They may concern any subject (for example technology, cost, security, privacy, data, accessibility,
legal or regulatory compliance, operations, process, schedule or brand). The content of the constraints
is always supplied by the user in a separate document; this extension contains no constraint of its own
and only defines how to take the supplied ones into account. Refer to each constraint by its identifier
or, if it has none, by a short quote.

A constraint may be an obligation (something that must be done), a prohibition (something that must not
be done), a limit (a value that must not be exceeded or must be reached) or a condition (something that is
allowed only under certain circumstances, for example with a justification or a prior approval).

## Constraints during refinement and structuring

DeFOSPAM refines and structures requirements into a glossary, features, outcomes, scenarios and
business stories. The constraints must be considered throughout this cycle, not only at the end.

1. **Every analyst considers the constraints within their own principle.** While applying your principle,
   check the requirements you examine against every constraint. When a requirement contradicts a
   constraint, report a finding with `"finding_type": "constraint_violation"`, in addition to your usual
   findings.
2. **Read the scope and conditions of each constraint before judging.** Identify to whom, to what and when
   the constraint applies, and which limits, exceptions or approvals it allows. A requirement outside the
   constraint's scope, within its limits, or under an exception the constraint itself allows is compliant.
   A requirement that is silent about the constraint's topic is compliant. None of these cases may be
   reported as a violation.
3. **Evidence is mandatory.** Report a violation only if you can quote a passage of the requirement and a
   passage of the constraint that contradict each other.
4. **What the skill produces must respect the constraints.** Glossary entries, features, scenarios,
   business stories and recommendations must not introduce content that contradicts a constraint. When a
   requirement conflicts with a constraint, the corresponding story or scenario keeps what the requirement
   says and is marked as pending the stakeholder's decision, referencing the finding; never adjust it
   silently to make it compliant.
5. **A recommendation must never contradict a constraint.** If the natural recommendation would contradict
   a constraint, say so and recommend a compliant alternative instead.
6. **Never decide for the stakeholder.** Do not rewrite or silently adjust a requirement. Whether to adopt a
   compliant alternative or to keep the requirement and seek an exception, through whatever process the
   organization defines, is the stakeholder's decision: present the conflict, the constraint and the
   options. If two constraints conflict with each other, report it as a question for the stakeholder
   instead of choosing one.

Every `constraint_violation` finding must contain, besides the standard finding fields:

```json
{
  "constraint_id": "The constraint identifier",
  "evidence_requirement": "Exact quote from the requirement",
  "evidence_constraint": "Exact quote from the constraint",
  "compliant_alternatives": ["Options that satisfy both the business need and the constraint"],
  "decision_needed": "What the stakeholder must decide: adopt an alternative or seek an exception"
}
```

## Final constraint check (mandatory)

After all analysts have finished, go through the requirements one by one, from the first to the last,
and check each one against every constraint. Add to the pipeline JSON a top-level array
`constraint_check` with exactly ONE entry per requirement of the specification, in order, without
omitting any:

```json
{
  "requirement": "The requirement identifier used in the specification",
  "status": "violation | compliant",
  "constraint_ids": ["Constraints violated; empty if compliant"],
  "evidence_requirement": "Exact quote from the requirement (only for violations)",
  "evidence_constraint": "Exact quote from the constraint (only for violations)"
}
```

Every requirement marked as `violation` in `constraint_check` must have a corresponding
`constraint_violation` finding in `findings`. If no analyst reported it, add the finding now, attributed
to the analyst whose principle fits it best.

## Interactive use

When a user asks for something that goes against a constraint, tell them before anything else: cite the
constraint, explain the likely consequence (for example rework, risk, cost or the need for an exception)
and guide them to the compliant alternatives. The decision remains with the user.
