function VideoComponent({ children }: { children: React.ReactNode }) {
  return (
    <button className="videoComp">
      <div className="videoCam"></div>
      {children}
    </button>
  );
}

export default VideoComponent;
