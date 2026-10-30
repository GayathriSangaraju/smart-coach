# UNShaken database ER diagram

Design for review; see [design](design.md) for confirmed requirements, technical
proposals, nullability, invariants, and remaining decisions. Mermaid does not
express cross-table ownership, mutually exclusive subtypes, or outcome checks.
The schema remains at 13 tables with no complete template-version subsystem.

```mermaid
erDiagram
    direction TB
    users ||--o{ user_identities : authenticates_with
    users ||--o{ custom_exercises : creates
    users o|--o{ workout_templates : owns
    users ||--o{ workout_sessions : performs
    exercise_categories ||--o{ exercises : categorizes
    body_parts ||--o{ exercises : classifies
    exercises ||--o| provider_exercises : provider_details
    exercises ||--o| custom_exercises : custom_details
    workout_templates ||--o{ template_exercises : contains
    exercises ||--o{ template_exercises : references
    template_exercises ||--o{ template_sets : plans
    workout_templates o|--o{ workout_sessions : starts
    workout_templates o|--o{ workout_sessions : applied_target
    workout_templates o|--o{ workout_templates : copied_from
    workout_sessions ||--o{ session_exercises : contains
    exercises ||--o{ session_exercises : references
    template_exercises o|--o{ session_exercises : source
    session_exercises ||--o{ session_sets : records
    template_sets o|--o{ session_sets : source
    users {
        uuid id PK
        string display_name
        string contact_email
        string preferred_weight_unit
        string status
        timestamptz created_at
        timestamptz updated_at
    }
    user_identities {
        uuid id PK
        uuid user_id FK
        string provider
        text issuer
        text subject
        string email_at_login
        boolean email_verified
        timestamptz last_login_at
        timestamptz created_at
    }
    exercise_categories {
        smallint id PK
        string name
        smallint sort_order
        boolean is_active
    }
    body_parts {
        smallint id PK
        string name
        smallint sort_order
        boolean is_active
    }
    exercises {
        uuid id PK
        string name
        smallint category_id FK
        smallint body_part_id FK
        string source_type
        text description
        boolean is_active
        timestamptz created_at
        timestamptz updated_at
    }
    provider_exercises {
        uuid exercise_id PK,FK
        string provider_name
        text provider_exercise_id
        text provider_body_part
        text provider_equipment
        jsonb instructions
        jsonb target_muscles
        jsonb secondary_muscles
        jsonb media_references
        jsonb raw_payload
        timestamptz last_synced_at
        timestamptz provider_updated_at
    }
    custom_exercises {
        uuid exercise_id PK,FK
        uuid created_by_user_id FK
    }
    workout_templates {
        uuid id PK
        uuid owner_user_id FK
        string template_type
        string name
        text notes
        uuid copied_from_template_id FK
        integer version
        timestamptz archived_at
        timestamptz created_at
        timestamptz updated_at
    }
    template_exercises {
        uuid id PK
        uuid template_id FK
        uuid exercise_id FK
        integer position
        text notes
    }
    template_sets {
        uuid id PK
        uuid template_exercise_id FK
        integer set_number
        integer target_reps
        decimal suggested_weight
        string weight_unit
        integer rest_seconds
    }
    workout_sessions {
        uuid id PK
        uuid user_id FK
        uuid source_template_id FK
        integer source_template_version
        string name_snapshot
        string status
        timestamptz started_at
        timestamptz finished_at
        text notes
        timestamptz template_updated_at
        boolean template_update_requested
        string template_update_status
        uuid applied_template_id FK
        timestamptz created_at
        timestamptz updated_at
    }
    session_exercises {
        uuid id PK
        uuid session_id FK
        uuid exercise_id FK
        uuid source_template_exercise_id FK
        string name_snapshot
        string category_snapshot
        string body_part_snapshot
        integer position
        text notes
    }
    session_sets {
        uuid id PK
        uuid session_exercise_id FK
        uuid source_template_set_id FK
        integer set_number
        integer target_reps_snapshot
        decimal suggested_weight_snapshot
        string suggested_weight_unit_snapshot
        integer actual_reps
        decimal actual_weight
        string weight_unit
        string status
        timestamptz completed_at
        integer rest_seconds
        boolean was_in_starting_plan
        timestamptz removed_at
        timestamptz rest_started_at
        timestamptz rest_ended_at
        timestamptz created_at
        timestamptz updated_at
    }
```

