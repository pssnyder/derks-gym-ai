# Port Configuration

## Port Usage in Derk's Gym AI Project

To avoid conflicts with the Steam version of Dr. Derk's Mutant Battlegrounds, we've changed the default port numbers used by the DerkAgentServer instances.

### Current Port Assignments

- **Player 1 Agent Server**: Port 9788 (changed from 8788)
- **Player 2 Agent Server**: Port 9789 (changed from 8789)

### Files Modified

1. `derks-starter-kit/run.py` - Main battle runner
2. `derks-starter-kit/custom_battle.py` - Custom battle runner with team configs

### Original Default Ports

The original Derk's Gym starter kit used:
- Port 8788 for Player 1
- Port 8789 for Player 2

### Reason for Change

These ports were changed to avoid potential conflicts when running both:
- The Steam version of Dr. Derk's Mutant Battlegrounds (for testing/analysis)
- Our custom AI training environment

### Technical Notes

The DerkAgentServer is used to create agent endpoints that communicate with the DerkAppInstance during battles. Each player needs its own port for the communication protocol.

### Future Considerations

If you need to change ports again:
1. Update both `run.py` and `custom_battle.py` files
2. Ensure ports don't conflict with:
   - Steam game instances
   - Other development tools
   - System reserved ports (0-1023)
   - Common application ports (3000, 5000, 8000, 8080, etc.)

### Recommended Port Ranges

- Development: 9000-9999
- Testing: 10000-10999
- Production: 11000-11999
