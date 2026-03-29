FROM rust:1.91 AS builder
WORKDIR /app

# Copy workspace root Cargo files
COPY rust/Cargo.toml rust/Cargo.lock ./

# Copy proto directory to parent (needed by proto-build build.rs ../../proto/)
COPY proto ../proto

# Copy all workspace members
COPY rust/proto-build ./proto-build
COPY rust/shared ./shared
COPY rust/services ./services

# Build the game service
RUN cargo build --release -p game

FROM debian:bookworm-slim
WORKDIR /app
RUN apt-get update && apt-get install -y libssl3 ca-certificates && rm -rf /var/lib/apt/lists/*
COPY --from=builder /app/target/release/game .

CMD ["./game"]
