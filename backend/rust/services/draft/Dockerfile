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


RUN cargo build --release -p draft

FROM debian:bookworm-slim
WORKDIR /app

COPY --from=builder /app/target/release/draft .

CMD ["./draft"]
