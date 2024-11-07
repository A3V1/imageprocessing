class UndoRedoManager:
    def __init__(self):
        self.history = []  # To store the history of states
        self.current_state = -1  # To track the current state index
    
    def add_state(self, state):
        """Add a new state to the history and update the current state."""
        # If we're in the middle of the history and adding a new state, remove any redo history
        self.history = self.history[:self.current_state + 1]  
        self.history.append(state)  
        self.current_state += 1  # Move to the new state

    def undo(self):
        """Undo to the previous state."""
        if self.current_state > 0:
            self.current_state -= 1  # Move back one step
            return self.history[self.current_state]  # Return the previous state
        return None  # No state to undo to
    
    def redo(self):
        """Redo to the next state."""
        if self.current_state < len(self.history) - 1:
            self.current_state += 1  # Move forward one step
            return self.history[self.current_state]  # Return the next state
        return None  # No state to redo to
    
    def reset(self):
        """Reset the history and current state."""
        self.history = []
        self.current_state = -1
