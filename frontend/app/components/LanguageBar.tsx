"use client";

interface LanguageData {
  lang: string;
  percent: number;
  color: string;
}

interface LanguageBarProps {
  languages: LanguageData[];
}

const LanguageBar: React.FC<LanguageBarProps> = ({ languages }) => {
  return (
    <div className="w-full h-4 flex rounded-md overflow-hidden border border-gray-700">
      {languages.map((l) => (
        <div
          key={l.lang}
          className="h-full"
          style={{
            width: `${l.percent}%`,
            backgroundColor: l.color,
          }}
          title={`${l.lang} ${l.percent.toFixed(1)}%`}
        />
      ))}
    </div>
  );
};

export default LanguageBar;
