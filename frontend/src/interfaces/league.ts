import { Team } from './team';

export interface League {
    leagueCode: string
    name: string
    teams: Team[]
    logo: string
}
