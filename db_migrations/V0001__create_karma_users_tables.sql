CREATE TABLE IF NOT EXISTS t_p72508054_karma_management_app.users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    subscription_plan VARCHAR(50) DEFAULT 'Росток'
);

CREATE TABLE IF NOT EXISTS t_p72508054_karma_management_app.goals (
    goal_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'active',
    target_date DATE
);

CREATE TABLE IF NOT EXISTS t_p72508054_karma_management_app.seeds (
    seed_id SERIAL PRIMARY KEY,
    goal_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    seed_name VARCHAR(255) NOT NULL,
    planted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    growth_level INTEGER DEFAULT 0,
    sprouts_count INTEGER DEFAULT 0,
    last_watered TIMESTAMP,
    water_streak_days INTEGER DEFAULT 0,
    total_actions INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS t_p72508054_karma_management_app.daily_actions (
    action_id SERIAL PRIMARY KEY,
    seed_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    action_type VARCHAR(100) NOT NULL,
    action_description TEXT,
    karma_points INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS t_p72508054_karma_management_app.merit_field (
    merit_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    good_deed_description TEXT NOT NULL,
    karma_impact INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    category VARCHAR(100)
);

CREATE INDEX IF NOT EXISTS idx_goals_user ON t_p72508054_karma_management_app.goals(user_id);
CREATE INDEX IF NOT EXISTS idx_seeds_goal ON t_p72508054_karma_management_app.seeds(goal_id);
CREATE INDEX IF NOT EXISTS idx_seeds_user ON t_p72508054_karma_management_app.seeds(user_id);
CREATE INDEX IF NOT EXISTS idx_actions_seed ON t_p72508054_karma_management_app.daily_actions(seed_id);
CREATE INDEX IF NOT EXISTS idx_actions_user ON t_p72508054_karma_management_app.daily_actions(user_id);
CREATE INDEX IF NOT EXISTS idx_merit_user ON t_p72508054_karma_management_app.merit_field(user_id);