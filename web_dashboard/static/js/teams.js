// Teams page JavaScript

class TeamsPage {
    constructor() {
        this.teams = {};
        this.relationships = {};
        this.derklings = {};
        this.init();
    }

    async init() {
        await this.loadData();
        this.renderTeamCompositions();
        this.renderRelationships();
        this.renderStrategyLoadouts();
    }

    async loadData() {
        try {
            const [teamsResponse, relationshipsResponse, derklingsResponse] = await Promise.all([
                fetch('/api/teams'),
                fetch('/api/relationships'),
                fetch('/api/derklings')
            ]);

            this.teams = await teamsResponse.json();
            this.relationships = await relationshipsResponse.json();
            this.derklings = await derklingsResponse.json();
        } catch (error) {
            console.error('Error loading data:', error);
        }
    }

    renderTeamCompositions() {
        const container = document.getElementById('team-compositions');
        if (!container) return;

        container.innerHTML = '';

        Object.entries(this.teams).forEach(([teamName, members]) => {
            const teamCard = this.createTeamCompositionCard(teamName, members);
            container.appendChild(teamCard);
        });
    }

    createTeamCompositionCard(teamName, members) {
        const div = document.createElement('div');
        div.className = 'card mb-4';
        
        const teamDisplayName = teamName.replace('_', ' ').toUpperCase();
        
        div.innerHTML = `
            <div class="card-header team-${teamName}">
                <h4 class="mb-0 text-white">
                    <i class="fas fa-shield-alt"></i> ${teamDisplayName} TEAM
                </h4>
            </div>
            <div class="card-body">
                <div class="row">
                    ${members.map(member => `
                        <div class="col-md-4 mb-3">
                            <div class="card h-100">
                                <div class="card-body">
                                    <div class="d-flex align-items-center mb-2">
                                        <div class="color-preview" style="background: ${member.colors.primary}"></div>
                                        <div class="color-preview" style="background: ${member.colors.secondary}"></div>
                                        <h6 class="mb-0 ms-2">${member.display_name}</h6>
                                    </div>
                                    <span class="role-badge">${member.role}</span>
                                    <p class="text-muted mt-2 mb-0">${this.derklings[member.name.toLowerCase()]?.specialty || 'Specialized fighter'}</p>
                                </div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;

        return div;
    }

    renderRelationships() {
        const container = document.getElementById('team-relationships');
        if (!container) return;

        container.innerHTML = '';

        Object.entries(this.relationships).forEach(([teamName, teamData]) => {
            if (teamData.bonds) {
                const relationshipCard = this.createRelationshipCard(teamName, teamData);
                container.appendChild(relationshipCard);
            }
        });
    }

    createRelationshipCard(teamName, teamData) {
        const div = document.createElement('div');
        div.className = 'card mb-4';
        
        const teamDisplayName = teamName.replace('_', ' ').toUpperCase();
        
        div.innerHTML = `
            <div class="card-header">
                <h5><i class="fas fa-heart"></i> ${teamDisplayName} Fighter Bonds</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    ${Object.entries(teamData.bonds).map(([fighter, bonds]) => `
                        <div class="col-md-6 mb-3">
                            <div class="card bg-light">
                                <div class="card-body">
                                    <h6 class="card-title">
                                        <i class="fas fa-user"></i> ${this.formatName(fighter)}
                                    </h6>
                                    <p class="text-muted mb-2">Bonds with:</p>
                                    ${bonds.map(bond => `
                                        <span class="badge bg-primary me-1">${this.formatName(bond)}</span>
                                    `).join('')}
                                    <p class="mt-2 mb-0">
                                        <small class="text-muted">
                                            <i class="fas fa-info-circle"></i>
                                            ${this.getBondDescription(fighter, bonds)}
                                        </small>
                                    </p>
                                </div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;

        return div;
    }

    renderStrategyLoadouts() {
        const container = document.getElementById('strategy-loadouts');
        if (!container) return;

        container.innerHTML = '';

        Object.entries(this.relationships).forEach(([teamName, teamData]) => {
            if (teamData.strategies) {
                const strategyCard = this.createStrategyCard(teamName, teamData.strategies);
                container.appendChild(strategyCard);
            }
        });
    }

    createStrategyCard(teamName, strategies) {
        const div = document.createElement('div');
        div.className = 'card mb-4';
        
        const teamDisplayName = teamName.replace('_', ' ').toUpperCase();
        
        div.innerHTML = `
            <div class="card-header">
                <h5><i class="fas fa-chess"></i> ${teamDisplayName} Strategy Loadouts</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    ${Object.entries(strategies).map(([strategyName, fighters]) => `
                        <div class="col-md-4 mb-3">
                            <div class="card border-primary">
                                <div class="card-header bg-primary text-white">
                                    <h6 class="mb-0">
                                        <i class="fas fa-${this.getStrategyIcon(strategyName)}"></i>
                                        ${strategyName.toUpperCase()}
                                    </h6>
                                </div>
                                <div class="card-body">
                                    ${fighters.map(fighter => `
                                        <div class="d-flex align-items-center mb-2">
                                            <i class="fas fa-arrow-right text-primary me-2"></i>
                                            <span>${this.formatName(fighter)}</span>
                                        </div>
                                    `).join('')}
                                    <small class="text-muted">
                                        ${this.getStrategyDescription(strategyName)}
                                    </small>
                                </div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;

        return div;
    }

    formatName(name) {
        return name.replace(/_/g, ' ')
                  .split(' ')
                  .map(word => word.charAt(0).toUpperCase() + word.slice(1))
                  .join(' ');
    }

    getBondDescription(fighter, bonds) {
        const descriptions = {
            'safe_t': 'Defensive specialist bonded with Spicy for perfect balance',
            'spicy': 'Aggressive fighter bonded with Safe T for perfect balance',
            'nightrider': 'Solo hunter similar to Angrrry, capable of solo or team combat',
            'angrrry': 'Versatile fighter similar to Nightrider, solo or team capable',
            'poonut': 'Decoy fighter, creates distractions in 3v3 with Safe T and Spicy',
            'the_assaulter': 'Pure assault tactics complement territory control',
            'the_engineer': 'Territory control pairs with assault and support strategies',
            'the_peacemaker': 'Support role enhances both assault and control tactics',
            'frank': 'Minimalist approach synergizes with experimental strategies',
            'number_eleven': 'Experimental tactics complement minimalist victory focus'
        };
        return descriptions[fighter] || 'Strategic partnership enhances combat effectiveness';
    }

    getStrategyIcon(strategy) {
        const icons = {
            'offensive': 'sword',
            'defensive': 'shield-alt',
            'balanced': 'balance-scale',
            'aggressive': 'fire',
            'control': 'chess-king',
            'support': 'hands-helping'
        };
        return icons[strategy] || 'chess-pawn';
    }

    getStrategyDescription(strategy) {
        const descriptions = {
            'balanced_3v3': 'Core 3v3 formation with decoy tactics',
            'solo_hunters': 'Flexible fighters capable of solo or team combat',
            'full_team': 'Complete peanut team deployment',
            'offensive': 'High-damage focus for quick eliminations',
            'defensive': 'Statue protection and territory control',
            'balanced': 'Versatile approach for any situation',
            'aggressive': 'Maximum pressure and enemy disruption',
            'control': 'Territory dominance and positioning',
            'support': 'Team enhancement and healing focus',
            'independent': 'Solo combat without team dependencies',
            'experimental': 'Cutting-edge tactics and strategies',
            'minimalist': 'Victory-focused with minimal complexity',
            'classified': 'Advanced experimental solo operations'
        };
        return descriptions[strategy] || 'Specialized tactical approach';
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new TeamsPage();
});
