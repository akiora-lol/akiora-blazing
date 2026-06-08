export interface Social {

    link: string;
    hidden: boolean;
}
export type SocialKey = "vk" | "tg" | "ds" | "yt" | "tw" | "sc"
export interface User {
    id: string;
    email: string;
    gender?: 'male' | 'female'
    nickname: string;
    age?: number;
    roles: Array<string>;
    socials: Record<SocialKey, Social[]>;
}

// Типы для League of Legends
export type LeagueServer =
    | 'EUW'
    | 'EUNE'
    | 'NA'
    | 'KR'
    | 'BR'
    | 'JP'
    | 'RU'
    | 'OCE'

    | 'TR';

export interface LeagueAccount {
    server: LeagueServer;
    gameName: string;
    tagLine: string;
    hidden?: boolean;
    // Дополнительные поля, которые можно добавить после верификации
    summonerId?: string;
    puuid?: string;
    profileIconId?: number;
    summonerLevel?: number;
}

// Состояние для нового аккаунта
export interface NewLeagueAccount extends LeagueAccount {
    // Можно добавить поля для валидации
}
