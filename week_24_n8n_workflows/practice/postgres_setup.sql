-- Run only in an isolated teaching database; no production data required.
CREATE TABLE IF NOT EXISTS course_tickets (
    ticket_id TEXT PRIMARY KEY, category TEXT NOT NULL,
    minutes_open INTEGER NOT NULL CHECK (minutes_open >= 0)
);
INSERT INTO course_tickets VALUES
  ('N101','access',120),('N102','billing',35),('N103','schedule',18),
  ('N105','other',240),('N106','billing',45)
ON CONFLICT (ticket_id) DO NOTHING;
-- Connect n8n with a role granted SELECT on course_tickets only.
