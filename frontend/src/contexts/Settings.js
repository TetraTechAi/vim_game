import React, { createContext, useContext, useState } from 'react';

const SettingsContext = createContext();

export function useSettings() {
  return useContext(SettingsContext);
}

export function SettingsProvider({ children }) {
  const [showCommand, setShowCommand] = useState(false);

  const value = {
    showCommand,
    setShowCommand,
  };

  return (
    <SettingsContext.Provider value={value}>
      {children}
    </SettingsContext.Provider>
  );
}
