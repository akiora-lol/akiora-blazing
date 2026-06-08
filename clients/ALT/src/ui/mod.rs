pub mod app;
pub mod components;
pub mod screens;
pub mod styles;

use app::App;
use ratatui::{prelude::*, widgets::*};
use std::io::{self, stdout, Stdout};

pub type Terminal = Terminal<CrosstermBackend<Stdout>>;
pub type Frame<'a> = Frame<'a>;

pub fn init() -> io::Result<Terminal> {
    let mut stdout = stdout();
    crossterm::terminal::enable_raw_mode()?;
    crossterm::event::EnableMouseCapture()?;
    crossterm::execute!(
        stdout,
        crossterm::event::EnableMouseCapture,
        crossterm::terminal::EnterAlternateScreen
    )?;
    let backend = CrosstermBackend::new(stdout);
    let terminal = Terminal::new(backend)?;
    Ok(terminal)
}

pub fn restore() -> io::Result<()> {
    let mut stdout = stdout();
    crossterm::terminal::disable_raw_mode()?;
    crossterm::event::DisableMouseCapture()?;
    crossterm::execute!(
        stdout,
        crossterm::event::DisableMouseCapture,
        crossterm::terminal::LeaveAlternateScreen
    )?;
    Ok(())
}