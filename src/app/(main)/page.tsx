import { VerseCard } from '@/components/app/verse-card';

export default function DashboardPage() {
  const verseOfTheDay = {
    reference: 'John 3:16',
    text: '“For God so loved the world, that he gave his only Son, that whoever believes in him should not perish but have eternal life.”',
    tags: ['Gospel', 'Atonement', 'Love', 'Faith'],
  };

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl md:text-4xl font-bold font-headline">Welcome to Sanctum</h1>
        <p className="text-lg text-muted-foreground">
          Here is your scheduled verse for today.
        </p>
      </div>
      <VerseCard
        reference={verseOfTheDay.reference}
        text={verseOfTheDay.text}
        tags={verseOfTheDay.tags}
      />
    </div>
  );
}
