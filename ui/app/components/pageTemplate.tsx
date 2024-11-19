import BackgroundSVG from "./BackgroundSVG";

function PageTemplate() {
  return (
    <div className="h-screen w-screen flex items-center justify-center outer-page">
      <div className="main_window bg-transparent">
        <BackgroundSVG />
        <div className="w-full h-full inside-Div"></div>
      </div>
    </div>
  );
}

export default PageTemplate;
