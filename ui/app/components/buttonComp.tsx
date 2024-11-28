function ButtonComponent({ children }: { children: React.ReactNode }) {
  return <button className="buttonComp backdrop-blur uppercase">{children}</button>;
}

export default ButtonComponent;
