// Derk's Gym AI Dashboard JavaScript

class DerklingDashboard {
    constructor() {
        this.derklings = {};
        this.teams = {};
        this.relationships = {};
        this.battleHistory = [];
        this.init();
    }

    async init() {
        await this.loadData();
        this.renderTeamCards();
        this.renderDerklingCards();
        this.updateStats();
    }

    async loadData() {
        try {
            // Load derkling data
            const derklingResponse = await fetch('/api/derklings');
            this.derklings = await derklingResponse.json();

            // Load team data
            const teamResponse = await fetch('/api/teams');
            this.teams = await teamResponse.json();

            // Load relationship data
            const relationshipResponse = await fetch('/api/relationships');
            this.relationships = await relationshipResponse.json();

            // Load battle history
            const battleResponse = await fetch('/api/battle_history');
            this.battleHistory = await battleResponse.json();

        } catch (error) {
            console.error('Error loading data:', error);
        }
    }

    renderTeamCards() {
        const container = document.getElementById('team-cards');
        if (!container) return;

        container.innerHTML = '';

        Object.entries(this.teams).forEach(([teamName, members]) => {
            const teamCard = this.createTeamCard(teamName, members);
            container.appendChild(teamCard);
        });
    }

    createTeamCard(teamName, members) {
        const col = document.createElement('div');
        col.className = 'col-md-6 col-lg-4 mb-3';

        const teamDisplayName = teamName.replace('_', ' ').toUpperCase();
        
        col.innerHTML = `
            <div class="card team-card">
                <div class="card-header team-${teamName}">
                    <h5 class="card-title mb-0">
                        <i class="fas fa-shield-alt"></i> ${teamDisplayName}
                    </h5>
                </div>
                <div class="card-body">
                    <p class="text-muted mb-2">${members.length} members</p>
                    <div class="member-list">
                        ${members.map(member => `
                            <div class="d-flex align-items-center mb-2">
                                <div class="color-preview" style="background: ${member.colors.primary}"></div>
                                <div>
                                    <strong>${member.display_name}</strong><br>
                                    <small class="text-muted">${member.role}</small>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
        `;

        return col;
    }

    renderDerklingCards() {
        const container = document.getElementById('derkling-cards');
        if (!container) return;

        container.innerHTML = '';

        Object.entries(this.derklings).forEach(([name, data]) => {
            const derklingCard = this.createDerklingCard(name, data);
            container.appendChild(derklingCard);
        });
    }

    createDerklingCard(name, data) {
        const col = document.createElement('div');
        col.className = 'col-md-6 col-lg-4 col-xl-3 mb-4';

        const teamSpiritPercent = Math.round(data.team_spirit * 100);
        const timeScalingPercent = Math.round(data.time_scaling * 100);

        col.innerHTML = `
            <div class="card derkling-card h-100">
                <div class="derkling-header team-${data.team}">
                    <h5 class="card-title mb-1">${data.display_name}</h5>
                    <span class="role-badge">${data.role}</span>
                </div>
                <div class="card-body">
                    <p class="specialty-text mb-3">${data.specialty}</p>
                    
                    <div class="mb-3">
                        <h6><i class="fas fa-palette"></i> Colors</h6>
                        <div class="d-flex align-items-center">
                            <div class="color-preview" style="background: ${data.colors.primary}"></div>
                            <div class="color-preview" style="background: ${data.colors.secondary}"></div>
                            <small class="text-muted">${data.colors.primary} / ${data.colors.secondary}</small>
                        </div>
                    </div>

                    <div class="mb-3">
                        <h6><i class="fas fa-tools"></i> Equipment</h6>
                        <div class="equipment-slots">
                            ${Object.entries(data.equipment).map(([slot, item]) => 
                                `<span class="equipment-slot">${slot}: ${item}</span>`
                            ).join('')}
                        </div>
                    </div>

                    <div class="mb-3">
                        <h6><i class="fas fa-heart"></i> Team Spirit</h6>
                        <div class="team-spirit-bar">
                            <div class="team-spirit-fill" style="width: ${teamSpiritPercent}%"></div>
                        </div>
                        <small class="text-muted">${teamSpiritPercent}%</small>
                    </div>

                    <div class="mb-3">
                        <h6><i class="fas fa-coins"></i> Key Bounties</h6>
                        <div class="bounty-list">
                            ${this.getKeyBounties(data.bounties).map(([key, value]) => `
                                <div class="bounty-item">
                                    <small>${this.formatBountyName(key)}</small>
                                    <span class="bounty-value ${value < 0 ? 'negative' : ''}">${value > 0 ? '+' : ''}${value}</span>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>
                <div class="card-footer">
                    <a href="/derkling/${name}" class="btn btn-outline-primary btn-sm">
                        <i class="fas fa-eye"></i> View Profile
                    </a>
                </div>
            </div>
        `;

        return col;
    }

    getKeyBounties(bounties) {
        // Get the most significant bounties for display
        const keyBounties = [
            'killEnemyUnit', 'killEnemyStatue', 'damageEnemyUnit', 'damageEnemyStatue',
            'healTeammate1', 'healTeammate2', 'victory', 'teamSpirit'
        ];
        
        return keyBounties
            .filter(key => bounties.hasOwnProperty(key))
            .map(key => [key, bounties[key]])
            .slice(0, 4); // Show top 4
    }

    formatBountyName(key) {
        const nameMap = {
            'killEnemyUnit': 'Kill Enemy',
            'killEnemyStatue': 'Kill Statue',
            'damageEnemyUnit': 'Damage Enemy',
            'damageEnemyStatue': 'Damage Statue',
            'healTeammate1': 'Heal Teammate',
            'healTeammate2': 'Heal Team 2',
            'victory': 'Victory',
            'teamSpirit': 'Team Spirit'
        };
        return nameMap[key] || key;
    }

    updateStats() {
        // Update dashboard statistics
        const totalDerklings = Object.keys(this.derklings).length;
        const activeTeams = Object.keys(this.teams).length;
        const battlesCompleted = this.battleHistory.length;
        
        // Calculate win rate (simplified - you might want more complex logic)
        let wins = 0;
        this.battleHistory.forEach(battle => {
            if (battle.winner) wins++;
        });
        const winRate = battlesCompleted > 0 ? Math.round((wins / battlesCompleted) * 100) : 0;

        // Update DOM elements
        this.updateElementText('total-derklings', totalDerklings);
        this.updateElementText('active-teams', activeTeams);
        this.updateElementText('battles-completed', battlesCompleted);
        this.updateElementText('win-rate', `${winRate}%`);
    }

    updateElementText(id, text) {
        const element = document.getElementById(id);
        if (element) {
            element.textContent = text;
        }
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new DerklingDashboard();
});
