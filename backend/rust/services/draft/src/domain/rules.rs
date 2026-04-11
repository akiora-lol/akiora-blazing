use shared::game::{Action, Command, Team};

const BP: Command = Command(Team::Blue(None), Action::Pick(None));
const BB: Command = Command(Team::Blue(None), Action::Ban(None));
const RP: Command = Command(Team::Red(None), Action::Pick(None));
const RB: Command = Command(Team::Red(None), Action::Ban(None));

pub const CLASSIC_5_DRAFT: [Command; 20] = [
    BB, RB, BB, RB, BB, RB, BP, RP, RP, BP, BP, RP, RB, BB, RB, BB, RP, BP, BP, RP,
];
