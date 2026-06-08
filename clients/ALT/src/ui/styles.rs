use ratatui::{prelude::*, style::Color, style::Modifier};

pub const PRIMARY_COLOR: Color = Color::Rgb(88, 101, 242);
pub const SUCCESS_COLOR: Color = Color::Green;
pub const ERROR_COLOR: Color = Color::Red;
pub const WARNING_COLOR: Color = Color::Yellow;
pub const BG_DARK: Color = Color::Rgb(15, 23, 42);
pub const BG_LIGHT: Color = Color::Rgb(30, 41, 59);
pub const TEXT_PRIMARY: Color = Color::Rgb(241, 245, 249);
pub const TEXT_SECONDARY: Color = Color::Rgb(148, 163, 184);

pub fn primary_style() -> Style {
    Style::default()
        .fg(PRIMARY_COLOR)
        .add_modifier(Modifier::BOLD)
}

pub fn success_style() -> Style {
    Style::default().fg(SUCCESS_COLOR)
}

pub fn error_style() -> Style {
    Style::default().fg(ERROR_COLOR)
}

pub fn warning_style() -> Style {
    Style::default().fg(WARNING_COLOR)
}

pub fn bg_dark_style() -> Style {
    Style::default().bg(BG_DARK)
}

pub fn bg_light_style() -> Style {
    Style::default().bg(BG_LIGHT)
}

pub fn text_primary_style() -> Style {
    Style::default().fg(TEXT_PRIMARY)
}

pub fn text_secondary_style() -> Style {
    Style::default().fg(TEXT_SECONDARY)
}

pub fn block_style() -> Block<'static> {
    Block::default()
        .bg(BG_LIGHT)
        .border_style(Style::default().fg(PRIMARY_COLOR))
        .borders(Borders::ALL)
}

pub fn title_style() -> Style {
    Style::default()
        .fg(PRIMARY_COLOR)
        .add_modifier(Modifier::BOLD)
}