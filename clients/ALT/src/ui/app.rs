use crate::ui::{screens::*, styles::*};
use ratatui::{
    prelude::*,
    widgets::{Block, Paragraph, Wrap},
};
use std::path::PathBuf;

#[derive(Debug, Clone, PartialEq)]
pub enum AppState {
    SplashScreen,
    Login,
    MainMenu,
    CreateLobby,
    JoinLobby,
    Settings,
    Exit,
}

#[derive(Debug, Clone)]
pub struct InputField {
    pub value: String,
    pub placeholder: String,
    pub focused: bool,
    pub max_length: Option<usize>,
}

impl Default for InputField {
    fn default() -> Self {
        Self {
            value: String::new(),
            placeholder: String::new(),
            focused: false,
            max_length: None,
        }
    }
}

impl InputField {
    pub fn new(placeholder: &str, max_length: Option<usize>) -> Self {
        Self {
            placeholder: placeholder.to_string(),
            max_length,
            ..Default::default()
        }
    }

    pub fn with_value(mut self, value: &str) -> Self {
        self.value = value.to_string();
        self
    }

    pub fn set_value(&mut self, value: &str) {
        if let Some(max_len) = self.max_length {
            self.value = value.chars().take(max_len).collect();
        } else {
            self.value = value.to_string();
        }
    }

    pub fn clear(&mut self) {
        self.value.clear();
    }

    pub fn len(&self) -> usize {
        self.value.len()
    }

    pub fn is_empty(&self) -> bool {
        self.value.is_empty()
    }
}

#[derive(Debug)]
pub struct App {
    pub state: AppState,
    pub email_input: InputField,
    pub code_input: InputField,
    pub lobby_name_input: InputField,
    pub lobby_password_input: InputField,
    pub error_message: Option<String>,
    pub session_path: Option<PathBuf>,
}

impl Default for App {
    fn default() -> Self {
        Self {
            state: AppState::SplashScreen,
            email_input: InputField::new("Email@example.com", Some(100)),
            code_input: InputField::new("Verification code", Some=6),
            lobby_name_input: InputField::new("Lobby name", Some=50),
            lobby_password_input: InputField::new("Lobby password", Some=20),
            error_message: None,
            session_path: None,
        }
    }
}

impl App {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn draw_splash_screen(&mut self, frame: &mut Frame) {
        let area = frame.size();

        let splash_text = "AKIORA ALT";
        let subtitle = "Terminal Game Client";

        let title = Paragraph::new(splash_text)
            .style(primary_style())
            .alignment(Alignment::Center);

        let subtitle = Paragraph::new(subtitle)
            .style(text_secondary_style())
            .alignment(Alignment::Center);

        frame.render_widget(
            Paragraph::new("")
                .block(block_style().title("")),
            area
        );

        let title_y = area.height / 2 - 2;
        let subtitle_y = area.height / 2;

        frame.render_widget(
            Block::default()
                .style(bg_dark_style())
                .borders(Borders::NONE),
            area
        );

        frame.render_widget(
            title,
            area.with_y(title_y)
        );

        frame.render_widget(
            subtitle,
            area.with_y(subtitle_y)
        );
    }

    pub fn draw_login_screen(&mut self, frame: &mut Frame) {
        let area = frame.size();

        let title = Paragraph::new("Login to Akiora")
            .style(title_style())
            .alignment(Alignment::Center);

        let email_block = InputField::widget(
            &self.email_input,
            "Email"
        );

        let code_block = InputField::widget(
            &self.code_input,
            "Verification Code"
        );

        let login_button = Paragraph::new("Login")
            .style(primary_style())
            .alignment(Alignment::Center);

        // Draw main container
        frame.render_widget(
            Block::default()
                .bg(BG_LIGHT)
                .borders(Borders::ALL)
                .border_style(Style::default().fg(PRIMARY_COLOR)),
            area
        );

        // Position elements
        let title_y = area.height / 4;
        frame.render_widget(title, area.with_y(title_y));

        let email_y = area.height / 2 - 2;
        frame.render_widget(email_block, area.with_y(email_y));

        let code_y = area.height / 2 + 2;
        frame.render_widget(code_block, area.with_y(code_y));

        let button_y = area.height * 3 / 4;
        frame.render_widget(login_button, area.with_y(button_y));

        // Draw error message if exists
        if let Some(error) = &self.error_message {
            let error_widget = Paragraph::new(error)
                .style(error_style())
                .alignment(Alignment::Center);
            let error_y = area.height - 3;
            frame.render_widget(error_widget, area.with_y(error_y));
        }
    }

    pub fn draw_main_menu(&mut self, frame: &mut Frame) {
        let area = frame.size();

        let title = Paragraph::new("Main Menu")
            .style(title_style())
            .alignment(Alignment::Center);

        let options = vec![
            "Create Lobby",
            "Join Lobby",
            "Settings",
            "Exit"
        ];

        let mut index = 0;
        for option in options {
            let style = if index == 0 {
                primary_style()
            } else {
                text_primary_style()
            };

            let widget = Paragraph::new(option)
                .style(style)
                .alignment(Alignment::Center);

            let y = area.height / 2 - 2 + index as u16;
            frame.render_widget(widget, area.with_y(y));
            index += 1;
        }

        frame.render_widget(
            Block::default()
                .bg(BG_LIGHT)
                .borders(Borders::ALL)
                .border_style(Style::default().fg(PRIMARY_COLOR)),
            area
        );

        let title_y = area.height / 4;
        frame.render_widget(title, area.with_y(title_y));
    }

    pub fn handle_input(&mut self, key: ratatui::crossterm::event::KeyEvent) {
        match self.state {
            AppState::Login => {
                match key.code {
                    ratatui::crossterm::event::KeyCode::Tab => {
                        // Toggle between email and code fields
                        if !self.email_input.focused {
                            self.email_input.focused = true;
                            self.code_input.focused = false;
                        } else {
                            self.email_input.focused = false;
                            self.code_input.focused = true;
                        }
                    }
                    ratatui::crossterm::event::KeyCode::Enter => {
                        // Handle login
                        if self.email_input.value.is_empty() {
                            self.error_message = Some("Please enter your email".to_string());
                        } else if self.code_input.value.is_empty() {
                            self.error_message = Some("Please enter verification code".to_string());
                        } else {
                            self.error_message = None;
                            self.state = AppState::MainMenu;
                        }
                    }
                    ratatui::crossterm::event::KeyCode::Backspace => {
                        if self.email_input.focused {
                            self.email_input.set_value(&self.email_input.value[..self.email_input.value.len().saturating_sub(1)]);
                        } else if self.code_input.focused {
                            self.code_input.set_value(&self.code_input.value[..self.code_input.value.len().saturating_sub(1)]);
                        }
                    }
                    ratatui::crossterm::event::KeyCode::Char(c) => {
                        if self.email_input.focused && (self.email_input.len() < self.email_input.max_length.unwrap_or(100)) {
                            self.email_input.set_value(&format!("{}{}", self.email_input.value, c));
                        } else if self.code_input.focused && self.code_input.len() < self.code_input.max_length.unwrap_or(6) {
                            self.code_input.set_value(&format!("{}{}", self.code_input.value, c));
                        }
                    }
                    _ => {}
                }
            }
            AppState::MainMenu => {
                match key.code {
                    ratatui::crossterm::event::KeyCode::Up => {
                        // Move selection up
                    }
                    ratatui::crossterm::event::KeyCode::Down => {
                        // Move selection down
                    }
                    ratatui::crossterm::event::KeyCode::Enter => {
                        // Handle menu selection
                    }
                    _ => {}
                }
            }
            _ => {}
        }
    }
}

impl InputField {
    pub fn widget(input: &Self, label: &str) -> Block<'static> {
        let title = format!("{}{}", label, if input.focused { " *" } else { "" });
        Block::default()
            .title(title)
            .borders(Borders::ALL)
            .border_style(if input.focused {
                primary_style()
            } else {
                text_secondary_style()
            })
    }
}