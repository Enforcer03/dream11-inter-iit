function ButtonComponent({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex flex-col items-center justify-center">
      <div className="my-1 anonymousPlayer"></div>
      <div className="my-1 anonymousPlayerText">{children}</div>
    </div>
  );
}

export default ButtonComponent;
