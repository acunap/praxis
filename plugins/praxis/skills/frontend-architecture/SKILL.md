---
name: frontend-architecture
description: Applies feature-based architecture for React frontends. Use when designing frontend structure, organizing components, hooks, and features, or when user mentions frontend architecture, React structure, or feature-based design.
---
icon: 🧩

# Frontend Architecture (Feature-Based)

## Boundary Rule

Something belongs inside a feature if it's only used by that feature. When a second feature needs it, promote to shared.

**Inside a feature**:
- Components specific to the feature
- Hooks that manage feature-specific state and logic

**Shared** (top-level):
- UI primitives (Button, Card, etc.)
- Hooks used by multiple features
- Utilities, API client

## File Structure

```
src/
  pages/
    HealthDashboard.tsx       # page: composes features, wiring
  features/
    health/
      components/
        HealthStatus.tsx      # component
      hooks/
        useHealthStatus.ts    # hook (fetch + state + logic, types inline)
      index.ts                # public API (barrel file)
  components/                 # shared UI components
  hooks/                      # shared hooks
  lib/                        # utilities, API client
  App.tsx                     # app shell, routing
  main.tsx                    # entry point
```

## Naming

- Page: PascalCase, screen name → `HealthDashboard.tsx`
- Feature folder: lowercase, noun → `health`, `settings`
- Component: PascalCase, descriptive → `HealthStatus.tsx`
- Hook: camelCase, `use` prefix → `useHealthStatus.ts`

## Colocation Principle

Start with everything inline. Extract only when a second consumer appears:

- **Types**: inline in the file that uses them. Extract to `types.ts` when shared across files in the feature.
- **API calls**: inline in the hook. Extract to `api.ts` when a second hook needs the same call.

## Separation of Concerns

- **Page** (`HealthDashboard`): Composes one or more features into a screen. Imported by App/router. No business logic.
- **Hook** (`useHealthStatus`): Data fetching, state management, error handling. All side effects live here.
- **Component** (`HealthStatus`): Renders UI based on props or hook return values. No direct fetch calls.

## Anti-Patterns

- **Fat components** — Components that fetch data, manage state, AND render UI. Extract logic into hooks.
- **Cross-feature imports** — Features importing directly from other features. If shared, promote to top-level.
- **Prop drilling** — Passing props through many layers. Use hooks closer to where data is needed.

## Implementation Order

Build from data to UI:

```
hook (with tests) → component → page → wiring in App
```

## Testing

- **Hooks**: Test with `renderHook`, mock fetch/API calls.
- **Components**: Test with Testing Library, provide hook data via props or mock hooks.
