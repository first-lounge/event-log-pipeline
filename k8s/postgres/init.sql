-- raw_events
CREATE TABLE IF NOT EXISTS raw_events (
    event_id        UUID        PRIMARY KEY,
    payload         JSONB       NOT NULL,
    processed_at    TIMESTAMPTZ
);

-- events
CREATE TYPE event_type AS ENUM ('page_view', 'purchase', 'error', 'click');

CREATE TABLE IF NOT EXISTS events (
    event_id    UUID            PRIMARY KEY,
    event_type  event_type      NOT NULL,
    user_id     INTEGER         NOT NULL,
    event_time  TIMESTAMPTZ     NOT NULL,
    page_name   VARCHAR(100)    NOT NULL,
    device      VARCHAR(50)     NOT NULL
);

-- purchase
CREATE TYPE payment_method AS ENUM ('card', 'pay', 'account');

CREATE TABLE IF NOT EXISTS purchase (
    event_id            UUID                PRIMARY KEY,
    price               BIGINT              NOT NULL,
    payment_method      payment_method      NOT NULL,
    product_id          BIGINT              NOT NULL,
    product_name        VARCHAR(255)        NOT NULL,
    product_category    VARCHAR(100)        NOT NULL,
    FOREIGN KEY (event_id) REFERENCES events(event_id)
);

-- error
CREATE TYPE error_level AS ENUM ('WARNING', 'ERROR', 'CRITICAL');

CREATE TABLE IF NOT EXISTS error (
    event_id        UUID            PRIMARY KEY,
    error_level     error_level     NOT NULL,
    error_code      INT             NOT NULL,
    error_msg       VARCHAR(100)    NOT NULL,
    FOREIGN KEY (event_id) REFERENCES events(event_id)
);

-- click
CREATE TABLE IF NOT EXISTS click (
    event_id            UUID            PRIMARY KEY,
    click_event_name    VARCHAR(100)    NOT NULL,
    element_type        VARCHAR(100)    NOT NULL,
    FOREIGN KEY (event_id) REFERENCES events(event_id)
);