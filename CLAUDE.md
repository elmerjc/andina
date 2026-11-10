# Odoo Development Project

## Stack

- Odoo 19 (Community + Enterprise)
- Python 3.12+
- PostgreSQL 16
- XML / QWeb
- JavaScript / OWL (Owl 2)
- Docker Compose
- Git

## Project layout

```
addons/          # Third-party Odoo addons
custom-addons/   # Custom modules (primary work area)
odoo/            # Odoo Enterprise modules (read-only unless requested)
config/          # odoo.conf
docker-compose.yaml
```

Each addon in `custom-addons/` must be independently installable.

## Core principles

- Never modify Odoo core unless explicitly requested.
- Extend models using `_inherit`. Extend views using XML inheritance.
- Reuse existing Odoo mechanisms before creating custom ones.
- Search `custom-addons/`, `addons/`, and `odoo/` before creating any new
  model, method, field, view, wizard, or utility.

## ORM

- Use the ORM. Avoid raw SQL unless ORM cannot reasonably solve the problem.
- Work with recordsets. Prefer batch operations.
- Avoid N+1 queries.
- Do not browse records repeatedly inside loops when the recordset can be prefetched.
- Use `sudo()` only when technically necessary; always add a comment explaining why.

## Python

- Follow [Odoo coding guidelines](https://www.odoo.com/documentation/19.0/contributing/development/coding_guidelines.html).
- Prefer readable code over clever code.
- Add comments only for non-obvious business or technical decisions.
- Keep methods focused and small.
- Do not refactor unrelated code.
- Call `super()` when overriding unless there is a documented reason not to.
- Preserve the expected return contract of overridden methods.

## XML / Views

- Prefer inherited views (`inherit_id`).
- Use XPath selectors — specific and stable.
- Never copy an entire view to change one element.
- Preserve existing XML style when modifying existing files.
- Do not change unrelated views.

## JavaScript / OWL

- Use OWL 2 patterns (Odoo 17+): `Component`, `useState`, `useService`, `onWillStart`, etc.
- Prefer extending existing Odoo components and services.
- Keep JavaScript changes minimal.
- Do not duplicate server-side business logic in JavaScript.
- Server-side permissions enforce security; UI hiding is not access control.

## Security

Every new model requires evaluation of:

- `ir.model.access.csv` — read/write/create/unlink per group
- Record rules — domain-based row-level security
- Groups — which group gets access
- Multi-company behavior — `company_id` field and domain filtering
- `sudo()` usage — documented and justified

Never assume hiding a UI element is a security mechanism.

## Git

Before modifying files:

1. `git status` — inspect current state
2. `git diff` — understand existing changes
3. Read only the relevant files

After modification:

1. `git diff` — verify only intended files changed
2. Confirm no unrelated files were touched

## Docker commands

```bash
# Start stack
docker compose up -d

# View Odoo logs
docker compose logs -f odoo-19

# Odoo shell
docker compose exec odoo-19 odoo shell -d msim

# Install / update module
docker compose exec odoo-19 odoo -d msim -i <module> --stop-after-init
docker compose exec odoo-19 odoo -d msim -u <module> --stop-after-init

# Run tests
docker compose exec odoo-19 odoo -d msim --test-enable -u <module> --stop-after-init
```

## Token efficiency

- Search first, then read only relevant files.
- Do not read the entire repository for a narrow task.
- Do not repeat commands whose result is already known.
- Do not explain unchanged code.
- Do not generate documentation unless requested.
- Do not create unnecessary abstractions.
- Prefer the smallest change that solves the problem.

## Completion criteria

A task is complete only when:

1. The requested behavior is implemented.
2. The code follows these rules.
3. Security has been evaluated if a model was added or modified.
4. The final `git diff` contains only intentional changes.
5. No unrelated refactoring was introduced.

If something cannot be verified, state exactly what could not be verified and why.